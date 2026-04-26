/**
 * Cloudflare Worker — прокси для Pexels API
 * Переменная окружения: PEXELS_KEY
 */

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, OPTIONS',
        },
      });
    }

    const url = new URL(request.url);
    const query = url.searchParams.get('query') || 'travel';
    const count = parseInt(url.searchParams.get('count') || '1', 10);
    const apiKey = env.PEXELS_KEY;

    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'PEXELS_KEY not set' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    try {
      const res = await fetch(
        `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=${count}&orientation=landscape`,
        { headers: { Authorization: apiKey } }
      );

      const data = await res.json();

      // Сохраняем src полностью — код ожидает photo.src.large2x и photo.src.large
      const photos = (data.photos || []).map(p => ({
        id: p.id,
        photographer: p.photographer,
        alt: p.alt,
        src: p.src,  // передаём как есть: { original, large2x, large, medium, small, tiny }
      }));

      return new Response(JSON.stringify({ photos }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600',
        },
      });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }
  },
};
