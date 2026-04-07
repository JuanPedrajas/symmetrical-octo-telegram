import { useItems } from "@/services/itemApi";

export function HomePage() {
  const { data: items, isLoading, error } = useItems();

  return (
    <main className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-8 text-3xl font-bold">App Template</h1>

      {isLoading && <p className="text-zinc-500">Loading items…</p>}

      {error && (
        <p className="text-red-600">
          Failed to load items: {(error as Error).message}
        </p>
      )}

      {items && items.length === 0 && (
        <p className="text-zinc-500">
          No items yet. Create one via the API at{" "}
          <code className="rounded bg-zinc-100 px-1 py-0.5 text-sm">
            POST /api/v1/items/
          </code>
        </p>
      )}

      {items && items.length > 0 && (
        <ul className="space-y-3">
          {items.map((item) => (
            <li
              key={item.id}
              className="rounded-lg border border-zinc-200 p-4"
            >
              <h2 className="font-semibold">{item.name}</h2>
              {item.description && (
                <p className="mt-1 text-sm text-zinc-600">
                  {item.description}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
