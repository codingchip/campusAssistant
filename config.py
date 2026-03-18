"""
配置文件 - 将敏感信息分离
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    KOZI_API_URL = os.getenv('KOZI_API_URL')
    KOZI_API_KEY = os.getenv('KOZI_API_KEY')
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 10))
    
    # 解析IP白名单
    allowed_ips = os.getenv('ALLOWED_IPS', '')
    ALLOWED_IPS = [ip.strip() for ip in allowed_ips.split(',') if ip.strip()] if allowed_ips else []
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """验证必要的配置是否存在"""
        required_vars = ['KOZI_API_URL', 'KOZI_API_KEY']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")
        
        print(f"配置验证通过，速率限制: {cls.RATE_LIMIT}次/分钟")
        if cls.ALLOWED_IPS:
            print(f"IP白名单已启用，允许 {len(cls.ALLOWED_IPS)} 个IP")
