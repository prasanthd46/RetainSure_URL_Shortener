from flask import Blueprint, abort, app, jsonify, redirect, request
from  app.models import store
from app.utils import generate_short_code, validate_url

bp = Blueprint('api', __name__)

@bp.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@bp.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


@bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        abort(400, description='Missing url field')

    url = data['url']
    if not validate_url(url):
        abort(400, description='Invalid url')


    code = store.find_code_for_url(url)
    if not code:
        code = generate_short_code(store.get_all_codes())
        store.save(code, url)

    short_url = request.host_url.rstrip('/') + '/' + code
    return jsonify({
        'short_code': code,
        'short_url': short_url
    }), 201


@bp.route('/<short_code>', methods=['GET'])
def redirect_short_code(short_code):
    
    mapping = store.get(short_code)
    if not mapping:
        abort(404, description="Short code not found")
        
    store.increment_click(short_code)
    return redirect(mapping.original_url , code=302)


@bp.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    
    mapping = store.get(short_code)
    if not mapping :
        abort(404, description="Short code not found")

    return jsonify({
        'url': mapping.original_url,
        'clicks': mapping.clicks,
        'created_at': mapping.created_at.isoformat()
    }), 200
