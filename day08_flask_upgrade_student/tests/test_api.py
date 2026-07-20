import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from app import app

@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client

# 1. 健康接口200
def test_health_check(test_client):
    res = test_client.get("/health")
    assert res.status_code == 200

# 2. 未登录访问接口被拦截302跳转登录
def test_metrics_no_login(test_client):
    res = test_client.get("/api/metrics")
    assert res.status_code == 302
    assert "/login" in res.location

# 3. 登录后正常获取指标数据
def test_metrics_login_success(test_client):
    # 模拟登录
    test_client.post("/login", data={"username": "student", "password": "day07"})
    res = test_client.get("/api/metrics")
    json_data = res.get_json()
    assert json_data["ok"] == True
    assert "metrics" in json_data

# 4. 品类筛选接口带参数过滤
def test_category_filter(test_client):
    test_client.post("/login", data={"username": "student", "password": "day07"})
    res = test_client.get("/api/categories?category=Fashion")
    json_data = res.get_json()
    assert json_data["ok"] == True
    assert json_data["category"] == "Fashion"
    assert len(json_data["rows"]) > 0