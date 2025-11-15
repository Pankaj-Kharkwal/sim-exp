"""
Block Registry - Auto-generated
Centralized registry of all available workflow blocks
"""

from typing import Dict, List, Any

# Block metadata imports
from app.executor.blocks.metadata.agent_meta import BLOCK_METADATA as AGENT_META
from app.executor.blocks.metadata.airtable_meta import BLOCK_METADATA as AIRTABLE_META
from app.executor.blocks.metadata.api_meta import BLOCK_METADATA as API_META
from app.executor.blocks.metadata.api_trigger_meta import BLOCK_METADATA as API_TRIGGER_META
from app.executor.blocks.metadata.arxiv_meta import BLOCK_METADATA as ARXIV_META
from app.executor.blocks.metadata.browser_use_meta import BLOCK_METADATA as BROWSER_USE_META
from app.executor.blocks.metadata.chat_trigger_meta import BLOCK_METADATA as CHAT_TRIGGER_META
from app.executor.blocks.metadata.clay_meta import BLOCK_METADATA as CLAY_META
from app.executor.blocks.metadata.condition_meta import BLOCK_METADATA as CONDITION_META
from app.executor.blocks.metadata.confluence_meta import BLOCK_METADATA as CONFLUENCE_META
from app.executor.blocks.metadata.discord_meta import BLOCK_METADATA as DISCORD_META
from app.executor.blocks.metadata.elevenlabs_meta import BLOCK_METADATA as ELEVENLABS_META
from app.executor.blocks.metadata.exa_meta import BLOCK_METADATA as EXA_META
from app.executor.blocks.metadata.file_meta import BLOCK_METADATA as FILE_META
from app.executor.blocks.metadata.firecrawl_meta import BLOCK_METADATA as FIRECRAWL_META
from app.executor.blocks.metadata.function_meta import BLOCK_METADATA as FUNCTION_META
from app.executor.blocks.metadata.generic_webhook_meta import BLOCK_METADATA as GENERIC_WEBHOOK_META
from app.executor.blocks.metadata.github_meta import BLOCK_METADATA as GITHUB_META
from app.executor.blocks.metadata.gmail_meta import BLOCK_METADATA as GMAIL_META
from app.executor.blocks.metadata.google_calendar_meta import BLOCK_METADATA as GOOGLE_CALENDAR_META
from app.executor.blocks.metadata.google_docs_meta import BLOCK_METADATA as GOOGLE_DOCS_META
from app.executor.blocks.metadata.google_drive_meta import BLOCK_METADATA as GOOGLE_DRIVE_META
from app.executor.blocks.metadata.google_forms_meta import BLOCK_METADATA as GOOGLE_FORMS_META
from app.executor.blocks.metadata.google_search_meta import BLOCK_METADATA as GOOGLE_SEARCH_META
from app.executor.blocks.metadata.google_sheets_meta import BLOCK_METADATA as GOOGLE_SHEETS_META
from app.executor.blocks.metadata.google_vault_meta import BLOCK_METADATA as GOOGLE_VAULT_META
from app.executor.blocks.metadata.guardrails_meta import BLOCK_METADATA as GUARDRAILS_META
from app.executor.blocks.metadata.huggingface_meta import BLOCK_METADATA as HUGGINGFACE_META
from app.executor.blocks.metadata.hunter_meta import BLOCK_METADATA as HUNTER_META
from app.executor.blocks.metadata.image_generator_meta import BLOCK_METADATA as IMAGE_GENERATOR_META
from app.executor.blocks.metadata.input_trigger_meta import BLOCK_METADATA as INPUT_TRIGGER_META
from app.executor.blocks.metadata.jina_meta import BLOCK_METADATA as JINA_META
from app.executor.blocks.metadata.jira_meta import BLOCK_METADATA as JIRA_META
from app.executor.blocks.metadata.knowledge_meta import BLOCK_METADATA as KNOWLEDGE_META
from app.executor.blocks.metadata.linear_meta import BLOCK_METADATA as LINEAR_META
from app.executor.blocks.metadata.linkup_meta import BLOCK_METADATA as LINKUP_META
from app.executor.blocks.metadata.manual_trigger_meta import BLOCK_METADATA as MANUAL_TRIGGER_META
from app.executor.blocks.metadata.mcp_meta import BLOCK_METADATA as MCP_META
from app.executor.blocks.metadata.mem0_meta import BLOCK_METADATA as MEM0_META
from app.executor.blocks.metadata.memory_meta import BLOCK_METADATA as MEMORY_META
from app.executor.blocks.metadata.microsoft_excel_meta import BLOCK_METADATA as MICROSOFT_EXCEL_META
from app.executor.blocks.metadata.microsoft_planner_meta import BLOCK_METADATA as MICROSOFT_PLANNER_META
from app.executor.blocks.metadata.microsoft_teams_meta import BLOCK_METADATA as MICROSOFT_TEAMS_META
from app.executor.blocks.metadata.mistral_parse_meta import BLOCK_METADATA as MISTRAL_PARSE_META
from app.executor.blocks.metadata.mongodb_meta import BLOCK_METADATA as MONGODB_META
from app.executor.blocks.metadata.mysql_meta import BLOCK_METADATA as MYSQL_META
from app.executor.blocks.metadata.notion_meta import BLOCK_METADATA as NOTION_META
from app.executor.blocks.metadata.number_meta import BLOCK_METADATA as NUMBER_META
from app.executor.blocks.metadata.onedrive_meta import BLOCK_METADATA as ONEDRIVE_META
from app.executor.blocks.metadata.openai_meta import BLOCK_METADATA as OPENAI_META
from app.executor.blocks.metadata.outlook_meta import BLOCK_METADATA as OUTLOOK_META
from app.executor.blocks.metadata.parallel_ai_meta import BLOCK_METADATA as PARALLEL_AI_META
from app.executor.blocks.metadata.perplexity_meta import BLOCK_METADATA as PERPLEXITY_META
from app.executor.blocks.metadata.pinecone_meta import BLOCK_METADATA as PINECONE_META
from app.executor.blocks.metadata.postgresql_meta import BLOCK_METADATA as POSTGRESQL_META
from app.executor.blocks.metadata.qdrant_meta import BLOCK_METADATA as QDRANT_META
from app.executor.blocks.metadata.reddit_meta import BLOCK_METADATA as REDDIT_META
from app.executor.blocks.metadata.resend_meta import BLOCK_METADATA as RESEND_META
from app.executor.blocks.metadata.response_meta import BLOCK_METADATA as RESPONSE_META
from app.executor.blocks.metadata.router_meta import BLOCK_METADATA as ROUTER_META
from app.executor.blocks.metadata.s3_meta import BLOCK_METADATA as S3_META
from app.executor.blocks.metadata.schedule_meta import BLOCK_METADATA as SCHEDULE_META
from app.executor.blocks.metadata.serper_meta import BLOCK_METADATA as SERPER_META
from app.executor.blocks.metadata.sharepoint_meta import BLOCK_METADATA as SHAREPOINT_META
from app.executor.blocks.metadata.slack_meta import BLOCK_METADATA as SLACK_META
from app.executor.blocks.metadata.sms_meta import BLOCK_METADATA as SMS_META
from app.executor.blocks.metadata.stagehand_agent_meta import BLOCK_METADATA as STAGEHAND_AGENT_META
from app.executor.blocks.metadata.stagehand_meta import BLOCK_METADATA as STAGEHAND_META
from app.executor.blocks.metadata.starter_meta import BLOCK_METADATA as STARTER_META
from app.executor.blocks.metadata.supabase_meta import BLOCK_METADATA as SUPABASE_META
from app.executor.blocks.metadata.tavily_meta import BLOCK_METADATA as TAVILY_META
from app.executor.blocks.metadata.telegram_meta import BLOCK_METADATA as TELEGRAM_META
from app.executor.blocks.metadata.thinking_meta import BLOCK_METADATA as THINKING_META
from app.executor.blocks.metadata.tool_type_1_meta import BLOCK_METADATA as TOOL_TYPE_1_META
from app.executor.blocks.metadata.translate_meta import BLOCK_METADATA as TRANSLATE_META
from app.executor.blocks.metadata.twilio_sms_meta import BLOCK_METADATA as TWILIO_SMS_META
from app.executor.blocks.metadata.typeform_meta import BLOCK_METADATA as TYPEFORM_META
from app.executor.blocks.metadata.variables_meta import BLOCK_METADATA as VARIABLES_META
from app.executor.blocks.metadata.vision_meta import BLOCK_METADATA as VISION_META
from app.executor.blocks.metadata.wait_meta import BLOCK_METADATA as WAIT_META
from app.executor.blocks.metadata.wealthbox_meta import BLOCK_METADATA as WEALTHBOX_META
from app.executor.blocks.metadata.webflow_meta import BLOCK_METADATA as WEBFLOW_META
from app.executor.blocks.metadata.webhook_meta import BLOCK_METADATA as WEBHOOK_META
from app.executor.blocks.metadata.whatsapp_meta import BLOCK_METADATA as WHATSAPP_META
from app.executor.blocks.metadata.wikipedia_meta import BLOCK_METADATA as WIKIPEDIA_META
from app.executor.blocks.metadata.workflow_input_meta import BLOCK_METADATA as WORKFLOW_INPUT_META
from app.executor.blocks.metadata.workflow_meta import BLOCK_METADATA as WORKFLOW_META
from app.executor.blocks.metadata.x_meta import BLOCK_METADATA as X_META
from app.executor.blocks.metadata.youtube_meta import BLOCK_METADATA as YOUTUBE_META
from app.executor.blocks.metadata.zep_meta import BLOCK_METADATA as ZEP_META

# Block registry mapping
BLOCK_REGISTRY: Dict[str, Dict[str, Any]] = {
    "agent": AGENT_META,
    "airtable": AIRTABLE_META,
    "api": API_META,
    "api_trigger": API_TRIGGER_META,
    "arxiv": ARXIV_META,
    "browser_use": BROWSER_USE_META,
    "chat_trigger": CHAT_TRIGGER_META,
    "clay": CLAY_META,
    "condition": CONDITION_META,
    "confluence": CONFLUENCE_META,
    "discord": DISCORD_META,
    "elevenlabs": ELEVENLABS_META,
    "exa": EXA_META,
    "file": FILE_META,
    "firecrawl": FIRECRAWL_META,
    "function": FUNCTION_META,
    "generic_webhook": GENERIC_WEBHOOK_META,
    "github": GITHUB_META,
    "gmail": GMAIL_META,
    "google_calendar": GOOGLE_CALENDAR_META,
    "google_docs": GOOGLE_DOCS_META,
    "google_drive": GOOGLE_DRIVE_META,
    "google_forms": GOOGLE_FORMS_META,
    "google_search": GOOGLE_SEARCH_META,
    "google_sheets": GOOGLE_SHEETS_META,
    "google_vault": GOOGLE_VAULT_META,
    "guardrails": GUARDRAILS_META,
    "huggingface": HUGGINGFACE_META,
    "hunter": HUNTER_META,
    "image_generator": IMAGE_GENERATOR_META,
    "input_trigger": INPUT_TRIGGER_META,
    "jina": JINA_META,
    "jira": JIRA_META,
    "knowledge": KNOWLEDGE_META,
    "linear": LINEAR_META,
    "linkup": LINKUP_META,
    "manual_trigger": MANUAL_TRIGGER_META,
    "mcp": MCP_META,
    "mem0": MEM0_META,
    "memory": MEMORY_META,
    "microsoft_excel": MICROSOFT_EXCEL_META,
    "microsoft_planner": MICROSOFT_PLANNER_META,
    "microsoft_teams": MICROSOFT_TEAMS_META,
    "mistral_parse": MISTRAL_PARSE_META,
    "mongodb": MONGODB_META,
    "mysql": MYSQL_META,
    "notion": NOTION_META,
    "number": NUMBER_META,
    "onedrive": ONEDRIVE_META,
    "openai": OPENAI_META,
    "outlook": OUTLOOK_META,
    "parallel_ai": PARALLEL_AI_META,
    "perplexity": PERPLEXITY_META,
    "pinecone": PINECONE_META,
    "postgresql": POSTGRESQL_META,
    "qdrant": QDRANT_META,
    "reddit": REDDIT_META,
    "resend": RESEND_META,
    "response": RESPONSE_META,
    "router": ROUTER_META,
    "s3": S3_META,
    "schedule": SCHEDULE_META,
    "serper": SERPER_META,
    "sharepoint": SHAREPOINT_META,
    "slack": SLACK_META,
    "sms": SMS_META,
    "stagehand_agent": STAGEHAND_AGENT_META,
    "stagehand": STAGEHAND_META,
    "starter": STARTER_META,
    "supabase": SUPABASE_META,
    "tavily": TAVILY_META,
    "telegram": TELEGRAM_META,
    "thinking": THINKING_META,
    "tool_type_1": TOOL_TYPE_1_META,
    "translate": TRANSLATE_META,
    "twilio_sms": TWILIO_SMS_META,
    "typeform": TYPEFORM_META,
    "variables": VARIABLES_META,
    "vision": VISION_META,
    "wait": WAIT_META,
    "wealthbox": WEALTHBOX_META,
    "webflow": WEBFLOW_META,
    "webhook": WEBHOOK_META,
    "whatsapp": WHATSAPP_META,
    "wikipedia": WIKIPEDIA_META,
    "workflow_input": WORKFLOW_INPUT_META,
    "workflow": WORKFLOW_META,
    "x": X_META,
    "youtube": YOUTUBE_META,
    "zep": ZEP_META,
}

def get_all_blocks() -> List[Dict[str, Any]]:
    """Get all registered blocks"""
    return list(BLOCK_REGISTRY.values())

def get_block_metadata(block_type: str) -> Dict[str, Any]:
    """Get metadata for a specific block type"""
    return BLOCK_REGISTRY.get(block_type)

def get_block_types() -> List[str]:
    """Get list of all block types"""
    return list(BLOCK_REGISTRY.keys())
