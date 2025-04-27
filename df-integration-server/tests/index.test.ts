import { describe, it, expect } from 'vitest';
import { DFIntegrationServer } from '../src/index.js';  // Adjust the import path as necessary

describe('DFIntegrationServer', () => {
  it('should initialize without errors', () => {
    const server = new DFIntegrationServer();
    expect(server).toBeDefined();
  });

  // Add more tests as needed, e.g., for tool handlers
});
