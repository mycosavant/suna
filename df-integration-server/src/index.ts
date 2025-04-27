import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListResourcesRequestSchema,
  ListResourceTemplatesRequestSchema,
  ListToolsRequestSchema,
  McpError,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';  // Example import for external API calls

const isValidForecastArgs = (
  args: any
): args is { city: string; days?: number } =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.city === 'string' &&
  (args.days === undefined || typeof args.days === 'number');

export class DFIntegrationServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'df-integration-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private isAuthenticated(request: any): boolean {
    return request.authToken === 'valid-token';  // Placeholder for actual authentication logic
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'get_agent_run',
          description: 'Start or manage an agent run',
          inputSchema: {
            type: 'object',
            properties: {
              workflow_id: { type: 'string' },
              context: { type: 'object' },
            },
            required: ['workflow_id'],
          },
        },
        {
          name: 'perform_code_analysis',
          description: 'Analyze code files',
          inputSchema: {
            type: 'object',
            properties: {
              file_path: { type: 'string' },
              related_files: { type: 'array', items: { type: 'string' } },
            },
            required: ['file_path'],
          },
        },
        {
          name: 'get_forecast',
          description: 'Get weather forecast for a city',
          inputSchema: {
            type: 'object',
            properties: {
              city: { type: 'string' },
              days: { type: 'number', minimum: 1, maximum: 5 },
            },
            required: ['city'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
      if (request.params.name === 'get_forecast') {
        if (!isValidForecastArgs(request.params.arguments)) {
          throw new McpError(ErrorCode.InvalidParams, 'Invalid forecast arguments');
        }
        return { content: [{ type: 'text', text: 'Forecast data' }] };
      } else if (request.params.name === 'get_agent_run') {
        const args = request.params.arguments as { workflow_id?: string; context?: object };
        if (!args.workflow_id) {
          throw new McpError(ErrorCode.InvalidParams, 'workflow_id is required');
        }
        if (!this.isAuthenticated(request)) {
          throw new McpError(ErrorCode.InvalidParams, 'Authentication required');
        }
        return { content: [{ type: 'text', text: `Agent run started for workflow ${args.workflow_id}` }] };
      } else if (request.params.name === 'perform_code_analysis') {
        const args = request.params.arguments as { file_path?: string; related_files?: string[] };
        if (!args.file_path) {
          throw new McpError(ErrorCode.InvalidParams, 'file_path is required');
        }
        if (!this.isAuthenticated(request)) {
          throw new McpError(ErrorCode.InvalidParams, 'Authentication required');
        }
        return { content: [{ type: 'text', text: `Analysis for ${args.file_path} completed` }] };
      }
      throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${request.params.name}`);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('DF Integration MCP server running on stdio');
  }
}

const server = new DFIntegrationServer();
server.run().catch(console.error);
