/**
 * CopilotKit API Route
 * 
 * This route acts as a proxy between CopilotKit's GraphQL frontend
 * and the ADK agent backend's REST API.
 */

import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";

// Backend URL from environment variable
const backendUrl = process.env.NEXT_PUBLIC_AGENT_URL || "http://localhost:8000";

// Create a CopilotRuntime instance configured with an HttpAgent that points
// to the ADK backend (AG-UI endpoint). This matches the pattern recommended
// in the CopilotKit blog for ADK + AG-UI integration.
const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    my_agent: new HttpAgent({ url: `${backendUrl}/api/copilotkit` }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
