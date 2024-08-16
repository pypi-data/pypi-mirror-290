import string
import json

# 英数字符和常见符号集合
en_and_common_symbols = string.ascii_letters + string.digits + string.punctuation + ' '
class LogEntry:
    def __init__(self, timestamp, domain_name, user_department, user_name, source_ip, session_id, action_type, developer, action_details=None, user_agent=None, resource_id=None):
        self.timestamp = timestamp
        self.domain_name = domain_name
        self.user_department = user_department
        self.user_name = user_name
        self.source_ip = source_ip
        self.session_id = session_id
        self.action_type = action_type
        self.developer = developer
        try:
            json_obj = json.loads(action_details)
            action_details = json.dumps(json_obj, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        self.action_details = action_details
        self.user_agent = user_agent
        self.resource_id = resource_id
        self._calculate_characters()

    def _calculate_characters(self):
        if self.action_type == "交談":
            self.ch_characters = self._calculate_ch_characters(self.action_details)
            self.en_characters = self._calculate_en_characters(self.action_details)
        elif self.action_type == "上傳檔案":
            # TODO: 計算檔案會花費的字元數
            self.ch_characters = 0
            self.en_characters = self._calculate_resource_characters(self.resource_id)
        else:
            self.ch_characters = 0
            self.en_characters = 0

        self.total_characters = self.ch_characters + self.en_characters

    def _calculate_ch_characters(self, str_detail):
        return sum(1 for char in str_detail if char not in en_and_common_symbols)

    def _calculate_en_characters(self, str_detail):
        return sum(1 for char in str_detail if char in en_and_common_symbols)
    
    def _calculate_resource_characters(self, resource_id):
        # TODO: 計算檔案會花費的字元數
        return 0

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "domain_name": self.domain_name,
            "user_department": self.user_department,
            "user_name": self.user_name,
            "source_ip": self.source_ip,
            "session_id": self.session_id,
            "action_type": self.action_type,
            "action_details": self.action_details,
            "user_agent": self.user_agent,
            "resource_id": self.resource_id,
            "developer": self.developer,
            "ch_characters": self.ch_characters,
            "en_characters": self.en_characters,
            "total_characters": self.total_characters,
        }