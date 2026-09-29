const GEMINI_MODEL = 'gemini-flash-latest';
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`;
const CATALOG = require('../data/data.json');
const CATALOG_BY_NAME = new Map(CATALOG.map(item => [item.name, item]));

const RESPONSE_SCHEMA = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    reason1: { type: 'string', maxLength: 40 },
    reason2: { type: 'string', maxLength: 40 }
  },
  required: ['name', 'reason1', 'reason2']
};

const SYSTEM_INSTRUCTION = `당신은 미술관 비교 화면의 추천 도우미입니다.
사용자가 준 후보 목록(최대 5개) 중에서 정확히 하나만 추천합니다.

지켜야 할 규칙:
- 후보 목록에 있는 이름만 그대로 씁니다. 후보 밖의 미술관을 말하지 않습니다.
- 이유에는 후보 표에 있는 방문객 수 · 국가 값만 씁니다. 숫자를 새로 만들거나 계산하지 않습니다.
- 표에 없는 정보(설립 연도 · 건축가 · 소장품 등)를 말하지 않습니다.
- 같은 후보 목록이 주어지면 항상 같은 곳을 추천합니다 — 후보 중 방문객 수가 가장 적어 조건 경계에 가장 가까운 곳부터 따져서 고릅니다.
- 반드시 지정된 JSON 스키마 형식으로만 답합니다. reason1 · reason2는 각각 한 줄입니다.`;

const LENGTH_INSTRUCTION = `Write reason1 and reason2 as one sentence each, with at most 40 characters per line. Use the candidate table's numbers to compare why the selected museum fits the condition; do not output numbers alone.`;

function extractText(payload) {
  const parts = payload && payload.candidates && payload.candidates[0]
    && payload.candidates[0].content && payload.candidates[0].content.parts;
  if (!Array.isArray(parts)) return null;
  const text = parts.map(p => p.text).filter(Boolean).join('');
  return text || null;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method_not_allowed' });
    return;
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: 'missing_key' });
    return;
  }

  const { minVisitors, country, candidates } = req.body || {};

  if (!Array.isArray(candidates) || candidates.length === 0 || candidates.length > 5) {
    res.status(400).json({ error: 'invalid_candidates' });
    return;
  }

  const candidatesMatchCatalog = candidates.every(candidate => {
    const source = CATALOG_BY_NAME.get(candidate && candidate.name);
    return source
      && source.visitors === candidate.visitors
      && source.country === candidate.country;
  });
  if (!candidatesMatchCatalog) {
    res.status(400).json({ error: 'invalid_candidates' });
    return;
  }

  const conditionText = [
    country ? `국가: ${country}` : null,
    minVisitors !== null && minVisitors !== undefined ? `최소 방문객 수: ${minVisitors}` : null
  ].filter(Boolean).join(' · ') || '조건 없음';

  const candidateText = candidates
    .map((c, i) => `${i + 1}. ${c.name} · 방문객 ${c.visitors} · ${c.country}`)
    .join('\n');

  const inputText = `조건 — ${conditionText}\n\n후보 목록(방문객 수 낮은 순):\n${candidateText}\n\n이 후보 중 하나를 추천하고, 이유 두 줄을 알려주세요.`;

  try {
    const response = await fetch(`${GEMINI_URL}?key=${encodeURIComponent(apiKey)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [
          { role: 'user', parts: [{ text: inputText }] }
        ],
        systemInstruction: {
          parts: [{ text: `${SYSTEM_INSTRUCTION}\n${LENGTH_INSTRUCTION}` }]
        },
        generationConfig: {
          responseMimeType: 'application/json',
          responseSchema: RESPONSE_SCHEMA
        }
      })
    });

    if (!response.ok) {
      if (response.status === 429) {
        res.status(429).json({ error: 'limit' });
        return;
      }
      res.status(502).json({ error: 'upstream_error', status: response.status });
      return;
    }

    const payload = await response.json();
    const text = extractText(payload);

    if (!text) {
      res.status(502).json({ error: 'no_text' });
      return;
    }

    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch (e) {
      res.status(502).json({ error: 'bad_json' });
      return;
    }

    const pickedNames = candidates.map(c => c.name);
    if (!parsed.name || !pickedNames.includes(parsed.name)) {
      res.status(200).json({ error: 'not_in_candidates', picked: parsed.name || null });
      return;
    }

    res.status(200).json({
      name: parsed.name,
      reason1: parsed.reason1 || '',
      reason2: parsed.reason2 || ''
    });
  } catch (err) {
    res.status(502).json({ error: 'call_failed' });
  }
};
