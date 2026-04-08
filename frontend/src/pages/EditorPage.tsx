import { useEffect, useState } from "react";
import { useSearchParams } from "react-router";
import { Button } from "@/components/ui/Button";
import { useFeatureDetail, useSaveFeature } from "@/services/featureApi";
import type { FeatureDetail, ScenarioModel, StepModel } from "@/types";

// ── Helpers ──────────────────────────────────────────────────────────────────

function extractTagValue(tags: string[], prefix: string): string {
  const tag = tags.find((t) => t.startsWith(`@${prefix}:`));
  return tag ? tag.slice(prefix.length + 2) : "";
}

function buildTags(entry: string, usecase: string, extra: string[]): string[] {
  const result: string[] = [];
  if (entry) result.push(`@entry:${entry}`);
  if (usecase) result.push(`@usecase:${usecase}`);
  return [...result, ...extra];
}

function getExtraTags(tags: string[]): string[] {
  return tags.filter((t) => !t.startsWith("@entry:") && !t.startsWith("@usecase:"));
}

const BACKGROUND_KEYWORDS = ["Given", "And", "But"];
const STEP_KEYWORDS = ["Given", "When", "Then", "And", "But"];

// ── Sub-components ────────────────────────────────────────────────────────────

function StepRow({
  step,
  keywords,
  onChange,
  onRemove,
}: {
  step: StepModel;
  keywords: string[];
  onChange: (s: StepModel) => void;
  onRemove: () => void;
}) {
  return (
    <div className="flex items-center gap-2">
      <select
        value={step.keyword}
        onChange={(e) => onChange({ ...step, keyword: e.target.value })}
        className="rounded border border-zinc-700 bg-zinc-800 px-2 py-1.5 text-sm text-zinc-200 focus:outline-none focus:ring-1 focus:ring-zinc-500"
      >
        {keywords.map((k) => (
          <option key={k} value={k}>
            {k}
          </option>
        ))}
      </select>
      <input
        type="text"
        value={step.text}
        onChange={(e) => onChange({ ...step, text: e.target.value })}
        placeholder="Step description…"
        className="flex-1 rounded border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
      />
      <button
        onClick={onRemove}
        className="text-zinc-500 hover:text-red-400 transition-colors"
        title="Remove step"
      >
        ✕
      </button>
    </div>
  );
}

function ScenarioCard({
  scenario,
  index,
  onChange,
  onRemove,
}: {
  scenario: ScenarioModel;
  index: number;
  onChange: (s: ScenarioModel) => void;
  onRemove: () => void;
}) {
  function updateStep(i: number, step: StepModel) {
    const steps = [...scenario.steps];
    steps[i] = step;
    onChange({ ...scenario, steps });
  }

  function addStep() {
    onChange({
      ...scenario,
      steps: [...scenario.steps, { keyword: "When", text: "" }],
    });
  }

  function removeStep(i: number) {
    const steps = scenario.steps.filter((_, idx) => idx !== i);
    onChange({ ...scenario, steps });
  }

  return (
    <div className="rounded-lg border border-zinc-700 bg-zinc-800/50 p-4 space-y-3">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 flex-1">
          <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wide shrink-0">
            Scenario {index + 1}
          </span>
          <input
            type="text"
            value={scenario.name}
            onChange={(e) => onChange({ ...scenario, name: e.target.value })}
            placeholder="Scenario name…"
            className="flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
          />
        </div>
        <button
          onClick={onRemove}
          className="text-zinc-500 hover:text-red-400 transition-colors text-sm"
          title="Remove scenario"
        >
          Remove
        </button>
      </div>

      <div className="space-y-2 pl-2 border-l border-zinc-700">
        {scenario.steps.map((step, i) => (
          <StepRow
            key={i}
            step={step}
            keywords={STEP_KEYWORDS}
            onChange={(s) => updateStep(i, s)}
            onRemove={() => removeStep(i)}
          />
        ))}
        <button
          onClick={addStep}
          className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          + Add step
        </button>
      </div>
    </div>
  );
}

// ── Main form state ───────────────────────────────────────────────────────────

interface FormState {
  featureName: string;
  description: string;
  entry: string;
  usecase: string;
  extraTags: string[];
  background: StepModel[];
  scenarios: ScenarioModel[];
}

function detailToForm(detail: FeatureDetail): FormState {
  return {
    featureName: detail.feature,
    description: detail.description,
    entry: extractTagValue(detail.tags, "entry"),
    usecase: extractTagValue(detail.tags, "usecase"),
    extraTags: getExtraTags(detail.tags),
    background: detail.background,
    scenarios: detail.scenarios,
  };
}

function formToDetail(form: FormState): FeatureDetail {
  return {
    feature: form.featureName,
    description: form.description,
    tags: buildTags(form.entry, form.usecase, form.extraTags),
    background: form.background,
    scenarios: form.scenarios,
  };
}

// ── EditorPage ────────────────────────────────────────────────────────────────

export function EditorPage() {
  const [searchParams] = useSearchParams();
  const path = searchParams.get("path");

  const { data: detail, isLoading, error } = useFeatureDetail(path);
  const { mutate: save, isPending: isSaving, isSuccess: saved, error: saveError } = useSaveFeature();

  const [form, setForm] = useState<FormState | null>(null);

  useEffect(() => {
    if (detail) setForm(detailToForm(detail));
  }, [detail]);

  function handleSave() {
    if (!form || !path) return;
    save({
      path,
      author: "Gherkins Bridge",
      data: formToDetail(form),
    });
  }

  if (!path) {
    return (
      <div className="flex h-full items-center justify-center text-zinc-500">
        No file selected.
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center text-zinc-500">
        Loading…
      </div>
    );
  }

  if (error || !form) {
    return (
      <div className="flex h-full items-center justify-center text-red-400">
        Failed to load: {(error as Error)?.message ?? "Unknown error"}
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center justify-between gap-4 border-b border-zinc-800 px-6 py-3 shrink-0">
        <p className="truncate text-xs text-zinc-500 font-mono">{path}</p>
        <div className="flex items-center gap-3 shrink-0">
          {saved && <span className="text-xs text-green-400">Saved ✓</span>}
          {saveError && (
            <span className="text-xs text-red-400">
              Error: {(saveError as Error).message}
            </span>
          )}
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? "Saving…" : "Save"}
          </Button>
        </div>
      </div>

      {/* Form */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-8">
        {/* ── Header Section ── */}
        <section className="space-y-4">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
            Header
          </h2>

          <div className="space-y-3">
            <div>
              <label className="mb-1 block text-xs text-zinc-400">Feature Name *</label>
              <input
                type="text"
                value={form.featureName}
                onChange={(e) => setForm({ ...form, featureName: e.target.value })}
                className="w-full rounded border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
                placeholder="e.g. Activate ASL Account"
              />
            </div>

            <div>
              <label className="mb-1 block text-xs text-zinc-400">Description</label>
              <textarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={3}
                className="w-full rounded border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 resize-y"
                placeholder="Optional feature description…"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1 block text-xs text-zinc-400">
                  @entry <span className="text-red-400">*</span>
                </label>
                <input
                  type="text"
                  value={form.entry}
                  onChange={(e) => setForm({ ...form, entry: e.target.value })}
                  className="w-full rounded border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
                  placeholder="e.g. npp"
                />
              </div>
              <div>
                <label className="mb-1 block text-xs text-zinc-400">
                  @usecase <span className="text-red-400">*</span>
                </label>
                <input
                  type="text"
                  value={form.usecase}
                  onChange={(e) => setForm({ ...form, usecase: e.target.value })}
                  className="w-full rounded border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
                  placeholder="e.g. activate_asl_account"
                />
              </div>
            </div>
          </div>
        </section>

        {/* ── Background Section ── */}
        <section className="space-y-3">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
            Background
          </h2>
          <div className="space-y-2 rounded-lg border border-zinc-800 bg-zinc-900/50 p-4">
            {form.background.map((step, i) => (
              <StepRow
                key={i}
                step={step}
                keywords={BACKGROUND_KEYWORDS}
                onChange={(s) => {
                  const background = [...form.background];
                  background[i] = s;
                  setForm({ ...form, background });
                }}
                onRemove={() => {
                  setForm({
                    ...form,
                    background: form.background.filter((_, idx) => idx !== i),
                  });
                }}
              />
            ))}
            <button
              onClick={() =>
                setForm({
                  ...form,
                  background: [
                    ...form.background,
                    { keyword: "Given", text: "" },
                  ],
                })
              }
              className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              + Add step
            </button>
          </div>
        </section>

        {/* ── Scenarios Section ── */}
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
              Scenarios
            </h2>
            <button
              onClick={() =>
                setForm({
                  ...form,
                  scenarios: [
                    ...form.scenarios,
                    { name: "", tags: [], steps: [{ keyword: "Given", text: "" }] },
                  ],
                })
              }
              className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              + Add scenario
            </button>
          </div>

          <div className="space-y-3">
            {form.scenarios.map((scenario, i) => (
              <ScenarioCard
                key={i}
                scenario={scenario}
                index={i}
                onChange={(s) => {
                  const scenarios = [...form.scenarios];
                  scenarios[i] = s;
                  setForm({ ...form, scenarios });
                }}
                onRemove={() =>
                  setForm({
                    ...form,
                    scenarios: form.scenarios.filter((_, idx) => idx !== i),
                  })
                }
              />
            ))}
            {form.scenarios.length === 0 && (
              <p className="text-sm text-zinc-600 italic">No scenarios yet.</p>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
