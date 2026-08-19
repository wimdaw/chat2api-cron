#!/usr/bin/env python3
"""ChatGPT Access Token 自动刷新脚本
部署为 GitHub Actions 定时任务: 每天执行, 用 session cookie 拿新 token 并上传到 chat2api

环境变量:
  SESSION_TOKEN: __Secure-next-auth.session-token 的值
  CHAT2API_URL: chat2api 服务地址
"""
import json, time, urllib.request, urllib.error, sys, os, urllib.parse

SESSION_TOKEN = os.environ.get("SESSION_TOKEN", "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..dUTm0BE30i_0Ld-x._-PwA2O6tRndARBp1k9o81ocddSNPI21e-VwWhDP_IURCjn5cx3bIdJbcN09kbRYW8eEoZA4vYZTweqy701hg1SUiquZDShJlbbb2Fz4g7deMlP87ZqNLm_LS9q-j19HjW4SXsr3j_FHkLJcBAJ7X7D6QeJTscw2Wk1mx1iJ4tLnptW9yr3Erh_W5P7grs11KJUy3A6cQn21_Hzwxp1LHaE5RUS7UyAzF9dZ8sy5UxuooRX_dpD2V9mWibPNl63L9_ivWb9kBUlYtyQEbvehfcezAy_yoPsFO3PlteNhkCYvQQNQ-DqaJXRr8faUvlk9Oygy4lz9bQZYiKSFq1iEmoOJ9EGCXeKhERaIUSE5QGtmwAEMa7VNA_grYoitpmZNL8id1AWlZARt4tq-0xqz44VitjiIor6qMtszSsEzH6r5opipjRXk7tOjcePWLbCYTCLCmDXR6kSq3_o2MAxhfD63ln0l0xiab4PXECafR47LDiBVgMF6MO2Ss-PQYJVtDxYQVREKofDfPXVNliyTxe0pAIziNiQFXeqaWMqIpJ-leMgcFw0kWHNwFqW77BVrUVx4D0ZzfYWY9DSztJerTnXLqNmGXzJO3-PK-PaoTOBqLeiquRUrWESGqGpxXj-G-p8opFf9-u_0BKmlsISG0Ps4EzNJq7i7JbLmfUyTQ_IGGYpucS1E4pi3RX4kNix3bHo9znQRzMWgrkkjZq5CIiMxhwHNxCzdPHaXZl4nyj__Nsd0wMsiVgdne8ZI2kXi2NkczKB1maLZvIvJ6-WeZTzp0EhSIf5P1J4Ou7aao9GYiTX0Uf6poQikhqKYuu-W5TDb4aA1hRurscQ6_shfU-PDfCoMovuKnjGIn5MpYbFkz6FD8IkAiei0eLaR6ipTqduADKYxQuHbNGAo1WiLvaz6rmB7yoeTJfTkzwpH8Zfp4TfGQpMNx-kv9TPsVAYcvhOJQYE3nJyNbC2CsUPfdIPhb9d4bMq-9xD9ib2LVEBa5x_FHLH65rZeCEMcMTiQEzBq_6z1w9DA0Jk2Fd1TwHEtWdw8_fZh6ErCont1noroNv8T9eJvAQODvJzwoIzaap3BUudB37XQpr-h6G6_G85r3opnKuZAEgCQwhDhLTButckjqlt50iXz2JjCe1r4eFSuEEWt-iM4WlXXn-tD4cETTnXerGkI20gc9kPTj9T5J2Y9KayzP_1ghhH2Sh0bH095C5Sur0W3Ba6-B7UTFzx3Tl2ChIBPBwO5OFJ0FP-ltrQ7O13Fey2KxL6UB-J9z-ojPyvKQRGOCc9VcOyKaIwt8Vqy_SSwxztm_DUiB2uKaY-K0c-yERt1CmE-riZtfGuKlpLbC70U9QF2yhhw-hzfdrtbCLkDkuGjaj83rBNSOHbMaPIQzIhn4TcXC8P9cNgiYeR--s5wtnzoG4uUTnlRRcGb_WDbDFdJETxT8LeSauAn1cEdb_xRs267OTthh9M5B7YLLF5683iuQ-IVlYijsO5qOCbMuuX6wKsMNicDdx0fnopA4OgCZV91fkFRe6yDfjBnw6uDwl29FTrw9y7GFQE9MO0IhgbR3BAMXFiRTrqTi3qlydico8EX5ZKedCvxDOYJvM-Ou13KpnPkQQw2VQH8h2SLgIrc72NOA76l5aLlTl04SNi9KZdzVI8YkGOTdZPBTATnSAR6WFCoyYzWaxop4jK60svhMGic5wsPVYbPoD7qUN52ukCNtavegAWFPB5bE6RjBubYwFocAAuWyY9v9l5cda5LV7HOxXsAQuFEFYwrYbUE5E51vU08JClvqwfL2Uumo3yfBi3oZVeOcG8Zaf9OdOX7BN9iSHp9VNPjeGJitSEloeEyJmh98T0ZPwf7h9Tp7L1pJ0wV4eCPCcj6ULcsaBNmQzmfPcdOSxk_rYSti-bqPj_CglwvDvUwSjL68PGQ67XnGeWe_UHYUu6i6SHD-1Ij3-K_Lon5weREJt6Pd1DpEeq_cDPJ1VF2RRP7JYCk5MhvKrVyDIKAEMVjZfiYapaHnu8yDbw0qGXlQBRRWbKwp0YgKe9_JyVEKRTgKvBSweqqD5IQ2ikYAXRuNMWWWbGuKdW7-xGeM_4mhc6Wj8IDJHT-fgAybVmH1Nskj1IAQqje1E4B3ld-LmZ4nj-S2x710xRBNPZa46kgO-Z11_fUiIBu2374by96VJdscYBrnRHgzjVT4HOj9yQGNROVMETQZf141s66y-MZvxFroxYvnzSSaBKpx1YEsuQvCHYMVz-K2XJtzyGitGkIdzfsfeZohygM7ikOUAXj8iGXuAgF5K7fShK78hIZ5y_gXeKhE0gGrtpZdNhNtqbGFaphqVzkt7jpKnZ-3i71Sxmh0bAf5CWLGXpgEki6xYjE8hAQVvEXT0BAmP6CLnOPZyYa_il2UdrvKqbDgvdWMn9oWkHqLe2Qn02f8K951vB73NieP0Upngop_ynGLnXPKXGfpQvcoiqJjfiSm3yuKpZscYheKOtLyAvLgNgKYP3D0UUHo4adMJxABq0wObtQztSiwQ5mAYT7BwNoOuq4YNqOmvRTaPyXWO9tRiAEuSgFtcuMzJ3rUDmCsfU1y5bGmjUcFyuBDAlGwGjy3I9DQS2LWlHFd4QMinzZFX7XoVjKgIhAx0JobOLY56Vbh4Fz2TMn04U1ThU8RMggWKT9-Xtcb0j28gltCTmtK1vM5b0Z_ZojU4_cq1MwvTqtuK-VtK3JLwHYPZB4vP9yx9sODPiqRApkEsz5larEU8vvDJaeuGju1VI5bRXj6IHPceKfujsVPTyM_HppPpKghgPI6m77fzpCYfwQv4T0zELs4k_kZPtqE905IlDhoUmDH5YQUEY22aEt_DRozt0AwQQQe9b8nNZUtvZrvcsWDDxksJPCoo2HUu1erGutbh7gZKpeGR_inu-6h1SfLDdFDDw-0LOWofoWhahn_MA7-8d6x_OSL-FjuzFuhmGK6Mco807sua7b1iC1S9wmYf_T2YIkRqysUshHtqGdU2D7RZKXScJpVpqwQt14DbdRFJ5yGtZltSG_ETgKUZn1IL0yK9vMM6nyybT3NGZY-f1JVkFXwJ12WJFgndsmpBesWY8iXaKmpCax0lguA57dH9tSfeUlg5sWMsUokiWtwxUVMY0lWt5jaC7khGraz0GRYv4D68ufKyPQk850CjYG8TcrD1s254VgIC4ClWpxDipNx34V4fs1fF5latEifeX4m59NZzFvZQYYuP7vP5ftE5lsYjMT6p8Dm2yDFZdeOOd1mTJh5kCgy6TcnDaGKD6Q12IxnZA-6JAHjlEHhK9AaXIjVg5kq5TR2K9BrHmPc2ahycivAT_EIqHHEQgl1pB1mUXM0sv2bKKaMaYerrXwE0xK8KfHa9tBYwLzwx-3UbEw_Lct8mrezmdWm04wKTR0eF3Nt1SkBtgKKw1JSbGoF_u83S53jgfUWZLlpNiXZs5XoVLB6VqY6uAHy0Q8wFDvFDZTeZerritzxXVH3JkQTdeso72lrqeUkpWArLNXTnoew02tnO3FHqPLd9mb51AcbnmTudLCzJKu3XqQLTx6UkxsAtmtbh3lXQOLWFhowQeaLDVNFCmTdZx7RTu4nAnMtdrTQUCpQR7mwleu_w.UyhHL3W_GiV6noZZHks9ng")
CHAT2API_URL = os.environ.get("CHAT2API_URL", "https://chat2api-hackerxiaow-c6f76b77.koyeb.app")

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def step1_check():
    """检查 chat2api 当前 token 是否还活着"""
    try:
        req = urllib.request.Request(f"{CHAT2API_URL}/v1/chat/completions", method="POST",
            headers={"Authorization": "Bearer fake", "Content-Type": "application/json"},
            data=json.dumps({"model":"gpt-4o","messages":[{"role":"user","content":"ping"}],"max_tokens":1}).encode())
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status == 200:
                log("✅ 当前 token 仍有效")
                return True
    except urllib.error.HTTPError as e:
        if e.code == 401:
            log("⚠️ 当前 token 已失效(401)")
            return False
    except Exception as e:
        log(f"⚠️ 检查异常: {e}")
    return None

def step2_get_new():
    """用 cookie 访问 chatgpt session 接口拿新 accessToken"""
    log("访问 chatgpt.com/api/auth/session...")
    req = urllib.request.Request("https://chatgpt.com/api/auth/session")
    req.add_header("Cookie", f"__Secure-next-auth.session-token={SESSION_TOKEN}")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
            if data and data.get("accessToken"):
                import base64
                at = data["accessToken"]
                parts = at.split(".")
                payload = parts[1] + "=" * (-len(parts[1]) % 4)
                exp = json.loads(base64.urlsafe_b64decode(payload)).get("exp", 0)
                left = exp - int(time.time())
                log(f"✅ 拿到新 accessToken ({len(at)}字符, 有效期{left//3600}h{(left%3600)//60}m)")
                return at
            else:
                log(f"❌ session 返回无 accessToken: {str(data)[:100]}")
                return None
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        log(f"❌ session 请求失败 HTTP {e.code}: {body}")
        return None
    except Exception as e:
        log(f"❌ session 请求异常: {e}")
        return None

def step3_upload(at):
    """上传新 token 到 chat2api"""
    log("上传 token 到 chat2api...")
    body = urllib.parse.urlencode({"text": at}).encode()
    req = urllib.request.Request(f"{CHAT2API_URL}/tokens/upload", data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            log(f"✅ 上传成功, token 数: {result.get('tokens_count','?')}")
            return True
    except Exception as e:
        log(f"❌ 上传失败: {e}")
        return False

def main():
    log("=== chat2api token 自动刷新 开始 ===")
    check = step1_check()
    if check is True:
        log("当前 token 仍有效, 提前续期防过期")
    new_at = step2_get_new()
    if not new_at:
        log("❌ 无法获取新 token, 流程终止")
        sys.exit(1)
    if step3_upload(new_at):
        log("=== 全部完成 ✅ ===")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
