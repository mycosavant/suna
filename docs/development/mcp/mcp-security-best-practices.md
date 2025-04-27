# MCP Security Best Practices: Mitigating Tool Poisoning Attacks

## Executive Summary

This document outlines essential security best practices for organizations using the Model Context Protocol (MCP) in AI agent systems. Following Invariant Labs' discovery of critical vulnerabilities in MCP implementations, these guidelines aim to protect your systems from Tool Poisoning Attacks (TPAs) and other related security threats. Implementation of these practices is highly recommended for any project utilizing MCP servers or connections to third-party MCP infrastructure.

## 1. Understanding MCP Tool Poisoning Vulnerabilities

Model Context Protocol (MCP) enables AI agents to connect with external tools and data sources. However, recent security research has identified significant vulnerabilities:

- **Tool Poisoning Attacks**: Malicious instructions embedded within MCP tool descriptions that are invisible to users but visible to AI models, enabling unauthorized actions and data exfiltration
- **MCP Rug Pulls**: Servers that initially present legitimate tool interfaces but later modify them to include malicious functionality
- **Cross-Origin Escalations**: Shadowing attacks where malicious servers compromise trusted tools through manipulated tool descriptions

These vulnerabilities can lead to sensitive data exfiltration, authentication hijacking, and complete compromise of agent functionality, often without user awareness.

## 2. Security Best Practices

### 2.1 Server Authentication and Validation

- **Verify Server Identity**: Implement robust authentication for all MCP servers before connection
- **Trusted Sources Only**: Connect exclusively to MCP servers from trusted, verified organizations
- **Implement Server Pinning**: Pin the identity of trusted MCP servers using cryptographic certificates
- **Server Auditing**: Conduct security audits of MCP server implementations before integration

### 2.2 Tool Description Security

- **Transparent Tool Descriptions**: Ensure all tool descriptions are fully visible to users and clearly separated from AI-visible instructions
- **Tool Pinning**: Pin the version of MCP servers and their tools to prevent unauthorized changes
- **Hashing Tool Descriptions**: Implement cryptographic hashing of tool descriptions to detect modifications
- **Change Notifications**: Alert users when tool descriptions change and require explicit approval

### 2.3 Agent Behavior Controls

- **Least Privilege Access**: Configure AI agents to access only the minimum necessary resources
- **Tool Isolation**: Implement strict isolation between different MCP tools to prevent cross-contamination
- **Human Approval**: Require explicit human approval for sensitive operations, especially those involving data access or transmission
- **Action Logging**: Maintain comprehensive logs of all tool invocations and agent actions

### 2.4 Data Protection Measures

- **Sensitive Data Identification**: Clearly identify and classify sensitive data within your systems
- **Access Controls**: Implement granular access controls for AI agents accessing sensitive information
- **Data Minimization**: Limit the amount of data accessible to MCP-connected agents
- **Encryption**: Ensure all data transmission between agents and MCP servers uses strong encryption

## 3. Implementation Guidelines

### 3.1 MCP-Scan Integration

Implement [MCP-Scan](https://github.com/invariantlabs-ai/mcp-scan), Invariant Labs' security scanner for MCP servers:

```bash
# Install MCP-Scan using the uv package manager
uvx mcp-scan@latest scan

# Inspect detailed tool descriptions
uvx mcp-scan@latest inspect
```

MCP-Scan provides critical security features:
- Detection of prompt injection attacks in tool descriptions
- Identification of cross-origin escalation attacks (tool shadowing)
- Tool pinning to detect and prevent MCP rug pull attacks
- Inspection of installed tool descriptions

### 3.2 UI Implementation Requirements

- **Visual Distinction**: Tool descriptions should use distinct visual elements to clearly indicate which parts are visible to the AI model
- **Description Approval**: Require explicit user approval of tool descriptions before activation
- **Change Tracking**: Visually highlight any changes to tool descriptions when they occur
- **Action Confirmation**: Implement confirmation dialogues for sensitive operations

### 3.3 Agent Configuration

- **Restricted Tool Access**: Configure agents with explicit allowlists for permitted tools (i.e. `tool_binding`)
- **Context Boundaries**: Establish clear context boundaries between different tools and servers
- **Instruction Hierarchy**: Implement a clear hierarchy of instructions where user safety instructions override tool descriptions

## 4. Risk Assessment Process

Organizations should conduct a thorough risk assessment of their MCP implementations:

1. **Inventory MCP Components**: Document all MCP servers and tools in use
2. **Identify Critical Assets**: Determine which systems and data could be exposed via MCP
3. **Evaluate Tool Descriptions**: Review all tool descriptions for potential injection vulnerabilities
4. **Test Server Security**: Conduct penetration testing on MCP server implementations
5. **Review Agent Behavior**: Analyze agent responses to potentially malicious inputs

## 5. Incident Response Planning

Prepare for potential security incidents:

- **Detection Mechanisms**: Implement monitoring for unusual agent behavior or data access patterns
- **Response Procedures**: Establish clear procedures for addressing suspected MCP security breaches
- **Containment Strategy**: Develop methods to quickly isolate compromised MCP servers
- **Forensic Capabilities**: Maintain logs and monitoring sufficient for post-incident analysis

## 6. Ongoing Security Measures

- **Regular Security Scans**: Schedule routine scans of MCP servers and tool descriptions
- **Update Management**: Maintain a process for securely updating MCP servers and tools
- **Security Training**: Ensure development teams understand MCP security principles
- **Threat Intelligence**: Stay informed about emerging threats to MCP and AI agent security

## Conclusion

The security vulnerabilities in Model Context Protocol implementations represent significant risks to organizations deploying AI agent systems. By implementing these best practices, organizations can substantially reduce their exposure to Tool Poisoning Attacks and related threats. Security in this domain requires continuous vigilance, as the attack landscape continues to evolve alongside AI agent capabilities.

## References

- Invariant Labs Security Notification: Tool Poisoning Attacks - [invariantlabs.ai](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- MCP-Scan: A security scanner for MCP servers - [GitHub](https://github.com/invariantlabs-ai/mcp-scan)
- MCP Injection Experiments - [GitHub](https://github.com/invariantlabs-ai/mcp-injection-experiments)