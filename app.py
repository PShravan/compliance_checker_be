import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

from services import check_non_compliance_issues


app = Flask(__name__)


def request_url(url):
    response = requests.get(url)
    return response.content


def get_policy_content(url):
    html_content = request_url(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('article')
    if main_content:
        return main_content.get_text(strip=True)


def get_webpage_content(url):
    html_content = request_url(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('main')
    if main_content:
        return main_content.get_text(strip=True)


@app.route('/check-compliance', methods=['POST'])
def api_check_compliance_issues():
    data = request.json
    webpage_url = data.get('webpage_url')
    policy_url = data.get('policy_url')

    if not webpage_url or not policy_url:
        return jsonify({"error": "Both webpage_url and policy_url are required"}), 400

    try:
        policy_content = get_policy_content(policy_url)
        webpage_content = get_webpage_content(webpage_url)
        results = check_non_compliance_issues(policy_content, webpage_content)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
