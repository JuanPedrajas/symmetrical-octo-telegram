import { useSearchParams } from "react-router";
import { FileTree } from "@/components/features/FileTree/FileTree";
import { EditorPage } from "@/pages/EditorPage";
import { useFeatureTree } from "@/services/featureApi";

export function HomePage() {
  const [searchParams] = useSearchParams();
  const selectedPath = searchParams.get("path") ?? undefined;
  const { data, isLoading, error } = useFeatureTree();

  return (
    <div className="flex h-screen overflow-hidden bg-zinc-950 text-zinc-200">
      {/* Sidebar */}
      <aside className="flex w-64 shrink-0 flex-col border-r border-zinc-800">
        <div className="border-b border-zinc-800 px-4 py-3">
          <h1 className="text-sm font-semibold text-zinc-200">Gherkins Bridge</h1>
          <p className="text-xs text-zinc-500">Feature file editor</p>
        </div>
        <div className="flex-1 overflow-y-auto py-2 px-1">
          {isLoading && <p className="px-3 text-xs text-zinc-500">Loading…</p>}
          {error && (
            <p className="px-3 text-xs text-red-400">
              Failed to load tree: {(error as Error).message}
            </p>
          )}
          {data && (
            <FileTree tree={data.tree} selectedPath={selectedPath} />
          )}
          {data && Object.keys(data.tree).length === 0 && (
            <p className="px-3 text-xs text-zinc-600 italic">
              No .feature files found in the repo.
            </p>
          )}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex flex-1 flex-col overflow-hidden">
        {selectedPath ? (
          <EditorPage />
        ) : (
          <div className="flex flex-1 items-center justify-center text-center">
            <div>
              <p className="text-zinc-500 text-sm">Select a feature file to edit</p>
              <p className="text-zinc-600 text-xs mt-1">Use the tree on the left to browse</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
