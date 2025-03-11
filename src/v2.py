import json
import random
import requests

def fetch_ips():
    """دریافت لیست آدرس های IP از یک URL."""
    try:
        response = requests.get('https://raw.githubusercontent.com/ircfspace/endpoint/refs/heads/main/ip.json')
        response.raise_for_status()  # بررسی وضعیت پاسخ HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"خطا در دریافت IPها: {e}")
        return {"ipv4": ["162.159.192.23:859", "162.159.192.178:4500"]}  # بازگشت IPهای پیش فرض در صورت خطا
    except json.JSONDecodeError as e:
         print(f"خطا در تجزیه پاسخ JSON: {e}")
         return {"ipv4": ["162.159.192.23:859", "162.159.192.178:4500"]}

def update_config_file(config_file):
    """به روز رسانی مقدار endpoint در فایل JSON."""
    try:
        with open(config_file, 'r') as f:
            data = json.load(f)

        ips = fetch_ips()
        ipv4_list = [ip for ip in ips.get('ipv4', []) if ip.startswith("162.")]

        if not ipv4_list:
            print("هیچ IP با شروع 162 پیدا نشد.")
            return

        new_endpoint = random.choice(ipv4_list)

        # پیدا کردن بخش outbounds و تنظیم endpoint
        if 'outbounds' in data:
            for outbound in data['outbounds']:
                if outbound.get('protocol') == 'wireguard' and 'settings' in outbound and 'peers' in outbound['settings']:
                    for peer in outbound['settings']['peers']:
                        if 'endpoint' in peer:
                            peer['endpoint'] = new_endpoint

        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Endpoint به {new_endpoint} تغییر یافت.")

    except FileNotFoundError:
        print(f"خطا: فایل {config_file} یافت نشد.")
    except json.JSONDecodeError:
        print(f"خطا: فایل {config_file} یک فایل JSON معتبر نیست.")
    except KeyError as e:
        print(f"خطا: ساختار فایل JSON مطابق انتظار نیست. کلید مفقود شده: {e}")
    except Exception as e:
        print(f"یک خطای غیرمنتظره رخ داد: {e}")
if __name__ == "__main__":
    config_file = 'oop.json'  # نام فایل JSON شما
    update_config_file(config_file)
