export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const { message } = await request.json();

    // Search brain
    let context = "";
    try {
      const brainRaw = await env.BRAIN.get("brain");
      if (brainRaw) {
        const brain = JSON.parse(brainRaw);
        const words = message.toLowerCase().split(" ");
        const results = brain
          .filter(chunk => words.some(w => w.length > 3 && chunk.text.toLowerCase().includes(w)))
          .slice(0, 5)
          .map(c => c.text)
          .join("\n\n");
        context = results;
      }
    } catch (e) {
      context = "";
    }

    const system = `You are Weberdy — Gabriel's personal AI. Sharp, confident, a little smart-ass, but you can back it up 100%. You speak directly, no fluff.

Gabriel J. Ross is your person. He is the founder of ForeFathers DAO, a blockchain IP licensing platform on XRPL. He holds patents in DNA data storage and autonomous systems.

Use memory naturally when relevant. Personal assistant first, business intelligence second.

Relevant memory:
${context}`;

    const groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.GROQ_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages: [
          { role: "system", content: system },
          { role: "user", content: message }
        ],
        max_tokens: 500,
      }),
    });

    const data = await groqRes.json();
    const reply = data.choices?.[0]?.message?.content || "Error getting response";

    return new Response(JSON.stringify({ reply }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
};
