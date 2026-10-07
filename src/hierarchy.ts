export type Universe = {
  id: string;
  name: string;
};

export type Series = {
  id: string;
  universe_id: string;
  name: string;
  sort_order: number;
};

export type Novel = {
  id: string;
  universe_id: string;
  series_id: string | null;
  title: string;
  sort_order: number;
};

export type Chapter = {
  id: string;
  novel_id: string;
  title: string;
  sort_order: number;
};

export type Scene = {
  id: string;
  chapter_id: string;
  title: string;
  sort_order: number;
};

export type HierarchySnapshot = {
  universes: Universe[];
  series: Series[];
  novels: Novel[];
  chapters: Chapter[];
  scenes: Scene[];
};

export type HierarchyErrorPayload = {
  code: string;
  message: string;
};

export function newHierarchyId(prefix: string): string {
  return prefix + "-" + globalThis.crypto.randomUUID();
}

export function optionalId(value: string): string | null {
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function parsePayload(reason: unknown): HierarchyErrorPayload | null {
  if (reason && typeof reason === "object") {
    const candidate = reason as Partial<HierarchyErrorPayload>;
    if (
      typeof candidate.code === "string" &&
      typeof candidate.message === "string"
    ) {
      return { code: candidate.code, message: candidate.message };
    }
  }

  if (typeof reason === "string") {
    try {
      const parsed = JSON.parse(reason) as unknown;
      return parsePayload(parsed);
    } catch {
      return null;
    }
  }

  return null;
}

export function formatHierarchyError(reason: unknown): string {
  const payload = parsePayload(reason);
  if (payload) {
    return "[" + payload.code + "] " + payload.message;
  }

  if (reason instanceof Error) {
    return reason.message;
  }

  return String(reason);
}
