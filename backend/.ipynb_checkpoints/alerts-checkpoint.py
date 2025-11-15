#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
Alert System - WhatsApp, Email, SMS with GPS Location
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import time
from geopy.geocoders import Nominatim
import requests

load_dotenv()


class AlertManager:
    """Manages all alert channels with GPS support"""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
        self.last_alert_time = 0
        self.alert_cooldown = int(os.getenv('ALERT_COOLDOWN', 300))
        self.alert_threshold = int(os.getenv('ALERT_THRESHOLD', 5))
        
        # Alert channel configs
        self.whatsapp_enabled = os.getenv('ENABLE_WHATSAPP', 'false').lower() == 'true'
        self.email_enabled = os.getenv('ENABLE_EMAIL', 'false').lower() == 'true'
        
        # GPS settings
        self.camera_lat = float(os.getenv('CAMERA_LATITUDE', 0))
        self.camera_lon = float(os.getenv('CAMERA_LONGITUDE', 0))
        self.camera_location = os.getenv('CAMERA_LOCATION', 'Unknown Location')
        
        # Initialize geocoder
        self.geolocator = Nominatim(user_agent="waste_detection_system")
        
        print(f"✓ Alert Manager initialized")
        print(f"  WhatsApp: {'ON' if self.whatsapp_enabled else 'OFF'}")
        print(f"  Email: {'ON' if self.email_enabled else 'OFF'}")
        print(f"  GPS: {self.camera_lat}, {self.camera_lon}")
    
    def should_send_alert(self, count: int) -> bool:
        """Check if alert should be sent"""
        current_time = time.time()
        
        if count < self.alert_threshold:
            return False
        
        if current_time - self.last_alert_time < self.alert_cooldown:
            return False
        
        return True
    
    def get_google_maps_link(self) -> str:
        """Generate Google Maps link for location"""
        if self.camera_lat and self.camera_lon:
            return f"https://maps.google.com/?q={self.camera_lat},{self.camera_lon}"
        return ""
    
    def get_location_address(self) -> str:
        """Get human-readable address from GPS coordinates"""
        try:
            if self.camera_lat and self.camera_lon:
                location = self.geolocator.reverse(f"{self.camera_lat}, {self.camera_lon}",



# In[5]:


"""
Production-Grade Alert System
WhatsApp, Email, SMS with GPS Location
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv()


class AlertManager:
    """Complete alert system with multiple channels"""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
        self.last_alert_time = 0
        self.alert_cooldown = int(os.getenv('ALERT_COOLDOWN', 300))
        self.alert_threshold = int(os.getenv('ALERT_THRESHOLD', 5))
        
        # Channel settings
        self.whatsapp_enabled = os.getenv('ENABLE_WHATSAPP', 'false').lower() == 'true'
        self.email_enabled = os.getenv('ENABLE_EMAIL', 'false').lower() == 'true'
        self.sms_enabled = os.getenv('ENABLE_SMS', 'false').lower() == 'true'
        
        # GPS settings
        self.camera_lat = float(os.getenv('CAMERA_LATITUDE', 0))
        self.camera_lon = float(os.getenv('CAMERA_LONGITUDE', 0))
        self.camera_location = os.getenv('CAMERA_LOCATION', 'Unknown Location')
        self.camera_name = os.getenv('CAMERA_NAME', 'Camera')
        
        # Alert counters
        self.total_alerts_sent = 0
        self.alerts_today = 0
        
        print("="*70)
        print("ALERT SYSTEM INITIALIZED")
        print("="*70)
        print(f"📍 Location: {self.camera_location}")
        print(f"🗺️  GPS: {self.camera_lat}, {self.camera_lon}")
        print(f"🚨 Alert Threshold: {self.alert_threshold} items")
        print(f"⏱️  Cooldown: {self.alert_cooldown}s ({self.alert_cooldown/60:.0f} min)")
        print(f"\nAlert Channels:")
        print(f"  WhatsApp: {'✅ ENABLED' if self.whatsapp_enabled else '❌ DISABLED'}")
        print(f"  Email:    {'✅ ENABLED' if self.email_enabled else '❌ DISABLED'}")
        print(f"  SMS:      {'✅ ENABLED' if self.sms_enabled else '❌ DISABLED'}")
        print("="*70 + "\n")
    
    def should_send_alert(self, count: int) -> bool:
        """Check if alert should be sent"""
        current_time = time.time()
        
        if count < self.alert_threshold:
            return False
        
        if current_time - self.last_alert_time < self.alert_cooldown:
            return False
        
        return True
    
    def get_google_maps_link(self) -> str:
        """Generate Google Maps link"""
        if self.camera_lat and self.camera_lon:
            return f"https://maps.google.com/?q={self.camera_lat},{self.camera_lon}"
        return ""
    
    def get_location_address(self) -> str:
        """Get human-readable address from GPS (requires internet)"""
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="waste_detection_system")
            location = geolocator.reverse(f"{self.camera_lat}, {self.camera_lon}", timeout=5)
            return location.address if location else self.camera_location
        except Exception as e:
            print(f"⚠️ Could not get address: {e}")
            return self.camera_location
    
    def send_whatsapp(self, count: int, confidence: float, detection_id: int) -> tuple:
        """Send WhatsApp alert via Twilio"""
        if not self.whatsapp_enabled:
            return False, "WhatsApp disabled in .env"
        
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_WHATSAPP_FROM')
            to_number = os.getenv('ALERT_WHATSAPP_TO')
            
            if not all([account_sid, auth_token, from_number, to_number]):
                return False, "Twilio credentials not configured"
            
            client = Client(account_sid, auth_token)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            maps_link = self.get_google_maps_link()
            
            message = f"""🚨 *PLASTIC WASTE ALERT*

📍 *Location:* {self.camera_location}
🗺️ GPS: {self.camera_lat}, {self.camera_lon}
🔗 {maps_link}

🗑️ *Waste Count:* {count} items
📊 *Confidence:* {confidence:.1%}
📹 *Camera:* {self.camera_name}
🕒 *Time:* {timestamp}
🔖 *Detection ID:* #{detection_id}

⚠️ *IMMEDIATE ACTION REQUIRED*
High waste accumulation detected!

Reply STOP to unsubscribe."""
            
            msg = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            print(f"✅ WhatsApp sent: {msg.sid}")
            return True, msg.sid
            
        except ImportError:
            return False, "Twilio library not installed. Run: pip install twilio"
        except Exception as e:
            print(f"❌ WhatsApp failed: {e}")
            return False, str(e)
    
    def send_email(self, count: int, confidence: float, detection_id: int, image_path: str = None) -> tuple:
        """Send Email alert with optional image attachment"""
        if not self.email_enabled:
            return False, "Email disabled in .env"
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.image import MIMEImage
            
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            from_email = os.getenv('EMAIL_FROM')
            password = os.getenv('EMAIL_PASSWORD')
            to_email = os.getenv('ALERT_EMAIL_TO')
            
            if not all([smtp_server, from_email, password, to_email]):
                return False, "Email credentials not configured"
            
            msg = MIMEMultipart('related')
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = f"🚨 Waste Alert - {count} items at {self.camera_location}"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            maps_link = self.get_google_maps_link()
            
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #d9534f 0%, #c9302c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .content {{
            padding: 30px;
        }}
        .alert-icon {{
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        .label {{
            font-weight: bold;
            color: #555;
            width: 40%;
        }}
        .value {{
            color: #333;
        }}
        .highlight {{
            background-color: #fff3cd;
            color: #d9534f;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .map-button {{
            display: inline-block;
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            margin: 20px 0;
        }}
        .map-button:hover {{
            background: linear-gradient(135deg, #0052a3 0%, #003d7a 100%);
        }}
        .warning {{
            background-color: #d9534f;
            color: white;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
        .image-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .image-container img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Plastic Waste Alert</h1>
        </div>
        
        <div class="content">
            <div class="alert-icon">⚠️</div>
            
            <div class="highlight">
                {count} PLASTIC ITEMS DETECTED
            </div>
            
            <table>
                <tr>
                    <td class="label">📍 Location</td>
                    <td class="value">{self.camera_location}</td>
                </tr>
                <tr>
                    <td class="label">🗺️ GPS Coordinates</td>
                    <td class="value">{self.camera_lat}, {self.camera_lon}</td>
                </tr>
                <tr>
                    <td class="label">📹 Camera</td>
                    <td class="value">{self.camera_name}</td>
                </tr>
                <tr>
                    <td class="label">📊 Detection Confidence</td>
                    <td class="value">{confidence:.1%}</td>
                </tr>
                <tr>
                    <td class="label">🕒 Detection Time</td>
                    <td class="value">{timestamp}</td>
                </tr>
                <tr>
                    <td class="label">🔖 Detection ID</td>
                    <td class="value">#{detection_id}</td>
                </tr>
            </table>
            
            <div style="text-align: center;">
                <a href="{maps_link}" class="map-button">
                    📍 View Location on Google Maps
                </a>
            </div>
            
            <div class="warning">
                ⚠️ IMMEDIATE ACTION REQUIRED
                <br>
                Please dispatch cleanup team to this location.
            </div>
        </div>
        
        <div class="footer">
            <p>Automated alert from Waste Detection System</p>
            <p>Detection ID: #{detection_id} | {timestamp}</p>
        </div>
    </div>
</body>
</html>
"""
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach image if available
            if image_path and Path(image_path).exists():
                try:
                    with open(image_path, 'rb') as f:
                        img_data = f.read()
                    image = MIMEImage(img_data, name=Path(image_path).name)
                    msg.attach(image)
                    print(f"   📎 Image attached: {Path(image_path).name}")
                except Exception as e:
                    print(f"   ⚠️ Could not attach image: {e}")
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False, str(e)
    
    def send_sms(self, count: int, confidence: float, detection_id: int) -> tuple:
        """Send SMS alert via Twilio"""
        if not self.sms_enabled:
            return False, "SMS disabled in .env"
        
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_SMS_FROM')
            to_number = os.getenv('ALERT_SMS_TO')
            
            if not all([account_sid, auth_token, from_number, to_number]):
                return False, "Twilio SMS credentials not configured"
            
            client = Client(account_sid, auth_token)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            maps_link = self.get_google_maps_link()
            
            message = f"""WASTE ALERT
{count} items at {self.camera_location}
Confidence: {confidence:.0%}
Time: {timestamp}
Map: {maps_link}
ID: #{detection_id}"""
            
            msg = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            print(f"✅ SMS sent: {msg.sid}")
            return True, msg.sid
            
        except Exception as e:
            print(f"❌ SMS failed: {e}")
            return False, str(e)
    
    def trigger_alert(self, detection_id: int, count: int, confidence: float, image_path: str = None):
        """Trigger all enabled alert channels"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        maps_link = self.get_google_maps_link()
        
        print("\n" + "="*70)
        print("🚨 ALERT TRIGGERED")
        print("="*70)
        print(f"Detection ID: #{detection_id}")
        print(f"Location: {self.camera_location}")
        print(f"GPS: {self.camera_lat}, {self.camera_lon}")
        print(f"Count: {count} items")
        print(f"Confidence: {confidence:.1%}")
        print(f"Time: {timestamp}")
        print(f"Maps: {maps_link}")
        print("="*70)
        
        # Console alert (always shown)
        console_msg = f"""
Location: {self.camera_location}
GPS: {self.camera_lat}, {self.camera_lon}
Camera: {self.camera_name}
Count: {count} items
Confidence: {confidence:.1%}
Time: {timestamp}
Detection ID: #{detection_id}
Maps: {maps_link}
        """
        
        # Save to database
        if self.db:
            try:
                self.db.save_alert({
                    'detection_id': detection_id,
                    'alert_type': 'console',
                    'message': console_msg,
                    'status': 'sent',
                    'recipient': 'console_output'
                })
            except Exception as e:
                print(f"⚠️ Could not save to database: {e}")
        
        alert_results = []
        
        # Send WhatsApp
        if self.whatsapp_enabled:
            print("\n📱 Sending WhatsApp...")
            success, result = self.send_whatsapp(count, confidence, detection_id)
            alert_results.append(('whatsapp', success, result))
            
            if self.db and success:
                try:
                    self.db.save_alert({
                        'detection_id': detection_id,
                        'alert_type': 'whatsapp',
                        'message': result,
                        'status': 'sent',
                        'recipient': os.getenv('ALERT_WHATSAPP_TO', 'N/A')
                    })
                except:
                    pass
        
        # Send Email
        if self.email_enabled:
            print("\n📧 Sending Email...")
            success, result = self.send_email(count, confidence, detection_id, image_path)
            alert_results.append(('email', success, result))
            
            if self.db and success:
                try:
                    self.db.save_alert({
                        'detection_id': detection_id,
                        'alert_type': 'email',
                        'message': result,
                        'status': 'sent',
                        'recipient': os.getenv('ALERT_EMAIL_TO', 'N/A')
                    })
                except:
                    pass
        
        # Send SMS
        if self.sms_enabled:
            print("\n💬 Sending SMS...")
            success, result = self.send_sms(count, confidence, detection_id)
            alert_results.append(('sms', success, result))
            
            if self.db and success:
                try:
                    self.db.save_alert({
                        'detection_id': detection_id,
                        'alert_type': 'sms',
                        'message': result,
                        'status': 'sent',
                        'recipient': os.getenv('ALERT_SMS_TO', 'N/A')
                    })
                except:
                    pass
        
        # Update counters
        self.last_alert_time = time.time()
        self.total_alerts_sent += 1
        self.alerts_today += 1
        
        # Summary
        print("\n" + "="*70)
        print("ALERT SUMMARY")
        print("="*70)
        for alert_type, success, msg in alert_results:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{alert_type.upper()}: {status}")
            if not success:
                print(f"  Reason: {msg}")
        print(f"\nTotal alerts sent today: {self.alerts_today}")
        print("="*70 + "\n")
        
        return alert_results
    
    def test_alerts(self):
        """Test all configured alert channels"""
        print("\n" + "="*70)
        print("TESTING ALERT SYSTEM")
        print("="*70)
        
        test_results = self.trigger_alert(
            detection_id=9999,
            count=10,
            confidence=0.95,
            image_path=None
        )
        
        return test_results


# ============ STANDALONE TEST ============
if __name__ == "__main__":
    print("Testing Alert System...\n")
    
    alert_mgr = AlertManager()
    
    print("\nRunning test alert in 3 seconds...")
    time.sleep(3)
    
    # Test alert
    results = alert_mgr.test_alerts()
    
    print("\n✓ Alert system test complete!")
    print("\nTo enable alerts:")
    print("1. Set ENABLE_WHATSAPP=true in .env")
    print("2. Set ENABLE_EMAIL=true in .env")
    print("3. Configure Twilio/Email credentials")
    print("4. Run detection system")


# In[1]:


"""
Complete Alert System - WhatsApp + Email
With DYNAMIC GPS Location
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import time
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from gps_location import GPSLocation

load_dotenv()


class AlertManager:
    """WhatsApp + Email alert system with dynamic GPS location"""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
        self.last_alert_time = 0
        self.alert_cooldown = int(os.getenv('ALERT_COOLDOWN', 300))
        self.alert_threshold = int(os.getenv('ALERT_THRESHOLD', 5))
        
        # Alert channel settings
        self.whatsapp_enabled = os.getenv('ENABLE_WHATSAPP', 'false').lower() == 'true'
        self.email_enabled = os.getenv('ENABLE_EMAIL', 'false').lower() == 'true'
        
        # GPS Location (Dynamic)
        self.gps = GPSLocation()
        self.camera_name = os.getenv('CAMERA_NAME', 'Mobile Camera')
        
        # Email credentials
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_to = os.getenv('ALERT_EMAIL_TO')
        
        # WhatsApp (Twilio) credentials
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.wa_from = os.getenv('TWILIO_WHATSAPP_FROM')
        self.wa_to = os.getenv('ALERT_WHATSAPP_TO')
        
        # Counters
        self.whatsapp_sent_today = 0
        self.email_sent_today = 0
        
        # Get initial location
        initial_location = self.gps.get_current_location()
        
        # Print status
        self._print_status(initial_location)
    
    def _print_status(self, location):
        """Print initialization status"""
        print("\n" + "="*70)
        print("🚨 ALERT SYSTEM INITIALIZED")
        print("="*70)
        print(f"📍 Current Location: {location['location']}")
        print(f"🗺️  GPS: {location['latitude']}, {location['longitude']}")
        print(f"📡 Source: {location['source']}")
        print(f"🚨 Threshold: {self.alert_threshold} items")
        print(f"⏱️  Cooldown: {self.alert_cooldown}s ({self.alert_cooldown/60:.0f} minutes)")
        
        print("\n📧 Email Alerts:")
        if self.email_enabled:
            print("   ✅ ENABLED")
            print(f"   To: {self.email_to}")
            if not all([self.smtp_server, self.email_from, self.email_password, self.email_to]):
                print("   ⚠️  WARNING: Missing email credentials")
        else:
            print("   ❌ DISABLED (Set ENABLE_EMAIL=true to enable)")
        
        print("\n📱 WhatsApp Alerts:")
        if self.whatsapp_enabled:
            print("   ✅ ENABLED")
            print(f"   To: {self.wa_to}")
        else:
            print("   ❌ DISABLED")
        
        print("="*70 + "\n")
    
    def get_current_location_info(self):
        """Get current location details"""
        return self.gps.get_current_location(force_refresh=True)
    
    def should_send_alert(self, count: int) -> bool:
        """Check if alert should be sent"""
        if count < self.alert_threshold:
            return False
        
        current_time = time.time()
        if current_time - self.last_alert_time < self.alert_cooldown:
            time_remaining = int(self.alert_cooldown - (current_time - self.last_alert_time))
            print(f"   ⏳ Cooldown active: {time_remaining}s remaining")
            return False
        
        return True
    
    def send_email(self, count: int, confidence: float, detection_id: int, image_path: str = None) -> tuple:
        """Send Email alert with CURRENT location"""
        
        if not self.email_enabled:
            return False, "Email disabled"
        
        if not all([self.smtp_server, self.email_from, self.email_password, self.email_to]):
            return False, "Missing email credentials in .env"
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.image import MIMEImage
            
            # Get CURRENT location
            location_info = self.get_current_location_info()
            
            msg = MIMEMultipart('related')
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f"🚨 Waste Alert - {count} items at {location_info['location']}"
            
            timestamp = datetime.now().strftime("%d %B %Y, %I:%M:%S %p")
            maps_link = self.gps.get_google_maps_link(location_info['latitude'], location_info['longitude'])
            
            # HTML email body
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 650px;
            margin: 20px auto;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .header {{
            background: linear-gradient(135deg, #d9534f 0%, #c9302c 100%);
            color: white;
            padding: 35px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: 600;
        }}
        .alert-icon {{
            font-size: 60px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 35px;
        }}
        .highlight-box {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffe4a0 100%);
            color: #d9534f;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
            border: 2px solid #ffc107;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }}
        .info-table td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        .info-label {{
            font-weight: 600;
            color: #555;
            width: 45%;
            font-size: 15px;
        }}
        .info-value {{
            color: #333;
            font-size: 15px;
        }}
        .map-button {{
            display: inline-block;
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white !important;
            padding: 14px 35px;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            font-size: 16px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,102,204,0.3);
        }}
        .warning-box {{
            background: linear-gradient(135deg, #d9534f 0%, #c9302c 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            margin-top: 25px;
            font-size: 16px;
            box-shadow: 0 4px 8px rgba(217,83,79,0.3);
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 25px;
            text-align: center;
            color: #666;
            font-size: 13px;
            border-top: 1px solid #e0e0e0;
        }}
        .gps-coords {{
            background-color: #e8f4f8;
            padding: 12px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #0066cc;
            margin: 10px 0;
        }}
        .location-badge {{
            display: inline-block;
            background-color: #5cb85c;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="alert-icon">⚠️</div>
            <h1>Plastic Waste Alert</h1>
        </div>
        
        <div class="content">
            <div class="highlight-box">
                🗑️ {count} PLASTIC ITEMS DETECTED
            </div>
            
            <table class="info-table">
                <tr>
                    <td class="info-label">📍 Current Location</td>
                    <td class="info-value">
                        <strong>{location_info['location']}</strong>
                        <span class="location-badge">🔴 LIVE</span>
                    </td>
                </tr>
                <tr>
                    <td class="info-label">🗺️ GPS Coordinates</td>
                    <td class="info-value">
                        <div class="gps-coords">
                            Lat: {location_info['latitude']:.6f}<br>
                            Lon: {location_info['longitude']:.6f}
                        </div>
                    </td>
                </tr>
                <tr>
                    <td class="info-label">📹 Camera</td>
                    <td class="info-value">{self.camera_name}</td>
                </tr>
                <tr>
                    <td class="info-label">📊 Detection Confidence</td>
                    <td class="info-value"><strong style="color: #5cb85c;">{confidence:.1%}</strong></td>
                </tr>
                <tr>
                    <td class="info-label">🕒 Detection Time</td>
                    <td class="info-value">{timestamp}</td>
                </tr>
                <tr>
                    <td class="info-label">🔖 Detection ID</td>
                    <td class="info-value">#{detection_id}</td>
                </tr>
            </table>
            
            <div style="text-align: center;">
                <a href="{maps_link}" class="map-button">
                    📍 View Current Location on Google Maps
                </a>
            </div>
            
            <div class="warning-box">
                ⚠️ IMMEDIATE ACTION REQUIRED<br>
                <span style="font-size: 14px; font-weight: normal; margin-top: 8px; display: block;">
                    Please dispatch cleanup team to the detected location immediately
                </span>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 5px 0;"><strong>Automated Alert</strong></p>
            <p style="margin: 5px 0;">Waste Detection System with Dynamic GPS</p>
            <p style="margin: 5px 0;">Detection ID: #{detection_id} | {timestamp}</p>
            <p style="margin: 5px 0; color: #999;">Location Source: {location_info['source']}</p>
        </div>
    </div>
</body>
</html>
"""
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach image if available
            if image_path and Path(image_path).exists():
                try:
                    with open(image_path, 'rb') as f:
                        img_data = f.read()
                    image = MIMEImage(img_data, name=Path(image_path).name)
                    msg.attach(image)
                    print(f"   📎 Image attached: {Path(image_path).name}")
                except Exception as e:
                    print(f"   ⚠️ Could not attach image: {e}")
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"   ✅ Email sent to {self.email_to}")
            self.email_sent_today += 1
            
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"   ❌ Email failed: {e}")
            return False, str(e)
    
    def trigger_alert(self, detection_id: int, count: int, confidence: float, image_path: str = None):
        """Trigger all enabled alert channels with CURRENT location"""
        
        # Get CURRENT location
        location_info = self.get_current_location_info()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        maps_link = self.gps.get_google_maps_link(location_info['latitude'], location_info['longitude'])
        
        print("\n" + "="*70)
        print("🚨 ALERT TRIGGERED")
        print("="*70)
        print(f"📍 Location: {location_info['location']}")
        print(f"🗺️  GPS: {location_info['latitude']:.6f}, {location_info['longitude']:.6f}")
        print(f"📡 Source: {location_info['source']}")
        print(f"🔗 Maps: {maps_link}")
        print(f"🗑️  Count: {count} items")
        print(f"📊 Confidence: {confidence:.1%}")
        print(f"🔖 Detection ID: #{detection_id}")
        print(f"🕒 Time: {timestamp}")
        print("="*70)
        
        alert_results = []
        
        # Send Email
        if self.email_enabled:
            print("\n📧 Sending Email...")
            success, result = self.send_email(count, confidence, detection_id, image_path)
            alert_results.append(('Email', success, result))
            
            # Save to database
            if self.db:
                try:
                    self.db.save_alert({
                        'detection_id': detection_id,
                        'alert_type': 'email',
                        'message': f"Sent to {self.email_to} - Location: {location_info['location']}",
                        'status': 'sent' if success else 'failed',
                        'recipient': self.email_to
                    })
                except:
                    pass
        
        # Update timestamp
        self.last_alert_time = time.time()
        
        # Summary
        print("\n" + "="*70)
        print("ALERT SUMMARY")
        print("="*70)
        
        success_count = 0
        for alert_type, success, msg in alert_results:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{alert_type}: {status}")
            if success:
                success_count += 1
            else:
                print(f"  Reason: {msg}")
        
        print(f"\nAlerts Sent Today:")
        print(f"  Email: {self.email_sent_today}")
        print("="*70 + "\n")
        
        return success_count > 0, location_info


# Test
if __name__ == "__main__":
    alert_mgr = AlertManager()
    
    response = input("\n⚠️  Send test alert? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        alert_mgr.trigger_alert(9999, 10, 0.95, None)


# In[ ]:




