from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent # This is use to create an agent that can perform tasks using the tools provided
from langchain.tools import tool # This is used to create a tool that can be used by the agent
from langchain_core.messages import HumanMessage # This is used to create a message that can be sent to the agent
from langchain_openai import ChatOpenAI # This is used to create a chat model that can be used by the agent
from langchain_tavily import TavilySearch


security_tool = TavilySearch(
    max_results=5,                        # Increased slightly to aggregate across multiple intel sources
    search_depth="advanced",              # Deep crawl for technical analysis & TTP breakdowns
    include_raw_content="markdown",       # Pulls markdown text to let the LLM analyze IOCs and Yara/Sigma rules
    include_answer=True,
    include_domains=[
        # --- Vendor CTI & Threat Research Labs ---
        "unit42.paloaltonetworks.com",    # Palo Alto Networks Unit 42 (APT & malware research)
        "mandiant.com",                   # Google Cloud / Mandiant Threat Intelligence 
        "talosintelligence.com",          # Cisco Talos (Vulnerabilities & global threat campaigns)
        "securelist.com",                 # Kaspersky Securelist (In-depth industrial and malware analysis)
        "research.checkpoint.com",        # Check Point Research (Campaign tracking & zero-days)
        "crowdstrike.com",                # CrowdStrike Intelligence (Adversary profiling & TTPs)
        "elastic.co",                     # Elastic Security Labs (Behavioral analytics & threat research)
        
        # --- Vulnerabilities, Frameworks & Standards ---
        "nvd.nist.gov",                   # National Vulnerability Database (CVE details & CVSS scores)
        "cve.mitre.org",                  # CVE official repository
        "attack.mitre.org",               # MITRE ATT&CK (Tactics, Techniques, and Procedures)
        "github.com",                     # Open-source detection rules, Sigma rules, and IOC repos
        
        # --- Industry Incident Reporting & News ---
        "bleepingcomputer.com",           # Rapid breach reporting and ransomware tracking
        "thehackernews.com",              # Emerging threat bulletins
        "exploit-db.com",                 # Exploit proof-of-concepts
        "cisa.gov"                        # CISA Cybersecurity Advisories & Known Exploited Vulnerabilities (KEV)
    ]
)

llm = ChatOpenAI(model="gpt-6-luna")
tools = [security_tool]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="Search for 3 threat actors currently attacking Australian Companies")})
    print(result)

if __name__ == "__main__":
    main()