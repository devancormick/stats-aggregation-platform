import Link from 'next/link'
import { getLeagues } from '@/lib/api'

export default async function Home() {
  const leagues = await getLeagues()

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12">
          <h1 className="text-4xl font-bold mb-2">Stats Aggregation Platform</h1>
          <p className="text-gray-600">Centralized stats for multiple leagues</p>
        </header>

        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-6">Featured Leagues</h2>
          {leagues.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
              No leagues available yet. Check back soon!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {leagues.map((league) => (
                <Link
                  key={league.id}
                  href={`/leagues/${league.slug}`}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
                >
                  {league.logo_url && (
                    <img
                      src={league.logo_url}
                      alt={league.name}
                      className="w-16 h-16 mb-4 object-contain"
                    />
                  )}
                  <h3 className="text-xl font-semibold mb-2">{league.name}</h3>
                  {league.description && (
                    <p className="text-gray-600 text-sm">{league.description}</p>
                  )}
                </Link>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  )
}
