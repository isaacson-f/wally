import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { StringEnum } from "@earendil-works/pi-ai";
import { Type, type Static } from "typebox";

type Section = {
  name: string;
  summary: string;
  members: Array<{
    name: string;
    signature: string;
    notes: string[];
  }>;
};

const sections: Section[] = [
  {
    name: "Events",
    summary: "Subscribe to Pi lifecycle, session, agent, model, input, and tool events.",
    members: [
      { name: "on", signature: "pi.on(eventName, handler)", notes: ["Handlers may inspect or alter some events.", "tool_call can block or mutate input; tool_result can patch output."] },
      { name: "events", signature: "pi.events.on(name, fn) / pi.events.emit(name, payload)", notes: ["Shared inter-extension event bus."] },
    ],
  },
  {
    name: "Tools",
    summary: "Register, inspect, override, and activate tools available to the model.",
    members: [
      { name: "registerTool", signature: "pi.registerTool(definition)", notes: ["Use TypeBox parameters.", "Use promptSnippet and promptGuidelines when the model needs tool-specific guidance.", "Throw from execute() to signal tool failure."] },
      { name: "getAllTools", signature: "pi.getAllTools()", notes: ["Returns built-in, SDK, and extension tools with sourceInfo."] },
      { name: "getActiveTools", signature: "pi.getActiveTools()", notes: ["Returns the active tool-name set for the current session."] },
      { name: "setActiveTools", signature: "pi.setActiveTools(names)", notes: ["Can switch Pi to restricted or expanded tool sets at runtime."] },
      { name: "exec", signature: "pi.exec(command, args, options?)", notes: ["Run shell commands from extensions without manually spawning child processes."] },
    ],
  },
  {
    name: "Commands and input",
    summary: "Add slash commands, shortcuts, flags, and programmatic messages.",
    members: [
      { name: "registerCommand", signature: "pi.registerCommand(name, { description, handler, getArgumentCompletions? })", notes: ["Command handlers receive ExtensionCommandContext with session-control helpers."] },
      { name: "getCommands", signature: "pi.getCommands()", notes: ["Lists extension commands, prompt templates, and skills available through prompt input."] },
      { name: "registerShortcut", signature: "pi.registerShortcut(key, { description, handler })", notes: ["Use documented keybinding names and avoid collisions where possible."] },
      { name: "registerFlag", signature: "pi.registerFlag(name, options)", notes: ["Adds extension-owned CLI flags."] },
      { name: "getFlag", signature: "pi.getFlag(name)", notes: ["Reads extension-owned CLI flag values."] },
      { name: "sendMessage", signature: "pi.sendMessage(customMessage, options?)", notes: ["Injects custom extension messages; optionally trigger a turn."] },
      { name: "sendUserMessage", signature: "pi.sendUserMessage(content, options?)", notes: ["Sends a real user message and triggers a turn."] },
    ],
  },
  {
    name: "Session state",
    summary: "Name sessions, append durable custom entries, and label branch points.",
    members: [
      { name: "appendEntry", signature: "pi.appendEntry(customType, data?)", notes: ["Persists extension state outside LLM context."] },
      { name: "setSessionName", signature: "pi.setSessionName(name)", notes: ["Sets the display name shown in session selectors."] },
      { name: "getSessionName", signature: "pi.getSessionName()", notes: ["Reads the current session display name."] },
      { name: "setLabel", signature: "pi.setLabel(entryId, label | undefined)", notes: ["Bookmarks entries for /tree navigation."] },
    ],
  },
  {
    name: "Models and providers",
    summary: "Register providers and control the active model and thinking level.",
    members: [
      { name: "registerProvider", signature: "pi.registerProvider(name, config)", notes: ["Supports OpenAI/Anthropic-style APIs, custom base URLs, headers, OAuth, and model lists."] },
      { name: "unregisterProvider", signature: "pi.unregisterProvider(name)", notes: ["Removes an extension-registered provider and restores built-ins where applicable."] },
      { name: "setModel", signature: "await pi.setModel(model)", notes: ["Returns false when required auth is unavailable."] },
      { name: "getThinkingLevel", signature: "pi.getThinkingLevel()", notes: ["Reads current reasoning effort: off/minimal/low/medium/high/xhigh."] },
      { name: "setThinkingLevel", signature: "pi.setThinkingLevel(level)", notes: ["Clamped to active model capabilities and emits thinking_level_select."] },
    ],
  },
  {
    name: "Rendering and UI",
    summary: "Customize message rendering and interact with the user through ExtensionContext UI helpers.",
    members: [
      { name: "registerMessageRenderer", signature: "pi.registerMessageRenderer(customType, renderer)", notes: ["Render messages produced by pi.sendMessage for the TUI."] },
      { name: "ctx.ui", signature: "ctx.ui.select / confirm / input / editor / notify / custom / setStatus / setWidget / setFooter / setTheme / setEditorComponent", notes: ["Available through event, tool, command, and shortcut contexts.", "Check ctx.hasUI in non-interactive modes."] },
    ],
  },
  {
    name: "Context helpers",
    summary: "Key data and controls available from handler contexts.",
    members: [
      { name: "ctx.sessionManager", signature: "ctx.sessionManager.getEntries() / getBranch() / getLeafId() / getSessionFile()", notes: ["Read-only view of session data."] },
      { name: "ctx.modelRegistry / ctx.model", signature: "ctx.modelRegistry.find(...) / ctx.model", notes: ["Inspect known models and the active model."] },
      { name: "ctx.getSystemPrompt", signature: "ctx.getSystemPrompt()", notes: ["Reads the current Pi system prompt string."] },
      { name: "ctx.getContextUsage", signature: "ctx.getContextUsage()", notes: ["Reads estimated/last known context usage."] },
      { name: "ctx.compact", signature: "ctx.compact({ customInstructions?, onComplete?, onError? })", notes: ["Triggers session compaction."] },
      { name: "ctx.abort / ctx.shutdown / ctx.isIdle / ctx.hasPendingMessages", signature: "ctx.abort(); ctx.shutdown(); ctx.isIdle(); ctx.hasPendingMessages()", notes: ["Control or inspect current agent runtime state."] },
    ],
  },
];

const formatMarkdown = (filter?: string) => {
  const needle = filter?.trim().toLowerCase();
  const selected = needle
    ? sections
        .map((section) => ({
          ...section,
          members: section.members.filter(
            (member) =>
              member.name.toLowerCase().includes(needle) ||
              member.signature.toLowerCase().includes(needle) ||
              member.notes.some((note) => note.toLowerCase().includes(needle)) ||
              section.name.toLowerCase().includes(needle),
          ),
        }))
        .filter((section) => section.members.length > 0 || section.name.toLowerCase().includes(needle))
    : sections;

  if (selected.length === 0) return `No pi object entries matched "${filter}".`;

  return [
    "# Wally Pi Object Reference",
    "",
    "A compact, extension-local reference for the Pi `ExtensionAPI` object and its most important context companions.",
    "",
    ...selected.flatMap((section) => [
      `## ${section.name}`,
      section.summary,
      "",
      ...section.members.flatMap((member) => [
        `### ${member.name}`,
        `\`${member.signature}\``,
        "",
        ...member.notes.map((note) => `- ${note}`),
        "",
      ]),
    ]),
  ].join("\n");
};

const WallySchema = Type.Object({
  format: Type.Optional(StringEnum(["markdown", "json"] as const)),
  filter: Type.Optional(Type.String({ description: "Only include entries matching this text." })),
});

type WallyInput = Static<typeof WallySchema>;

export default function wally(pi: ExtensionAPI) {
  pi.registerCommand("wally", {
    description: "Show a compact reference for the Pi extension API object.",
    handler: async (args, ctx) => {
      const text = formatMarkdown(args || undefined);
      if (ctx.hasUI) ctx.ui.notify(text, "info");
      else console.log(text);
    },
  });

  pi.registerTool({
    name: "wally_pi_reference",
    label: "Wally Pi Reference",
    description: "Return a comprehensive reference for the Pi ExtensionAPI object, including methods, events, tools, commands, sessions, models, and UI helpers.",
    promptSnippet: "Look up the Pi ExtensionAPI object and context helper reference.",
    promptGuidelines: ["Use wally_pi_reference when the user asks what the Pi object can do or how to write a Pi extension."],
    parameters: WallySchema,
    async execute(_toolCallId, params: WallyInput) {
      if (params.format === "json") {
        const needle = params.filter?.trim().toLowerCase();
        const payload = needle
          ? sections.map((section) => ({
              ...section,
              members: section.members.filter((member) =>
                JSON.stringify(member).toLowerCase().includes(needle) || section.name.toLowerCase().includes(needle),
              ),
            })).filter((section) => section.members.length > 0 || section.name.toLowerCase().includes(needle))
          : sections;
        return { content: [{ type: "text", text: JSON.stringify(payload, null, 2) }], details: { sections: payload } };
      }

      const text = formatMarkdown(params.filter);
      return { content: [{ type: "text", text }], details: { sections } };
    },
  });

  pi.on("session_start", (_event, ctx) => {
    if (ctx.hasUI) ctx.ui.setStatus("wally", "wally: /wally or tool wally_pi_reference");
  });

  pi.on("session_shutdown", (_event, ctx) => {
    if (ctx.hasUI) ctx.ui.setStatus("wally", undefined);
  });
}
