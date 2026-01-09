async function ask(){
  const status = document.getElementById("status");
  const answerBox = document.getElementById("answer");

  const question = document.getElementById("question").value.trim();
  const image = document.getElementById("image").files[0];
  const audio = document.getElementById("audio").files[0];

  if(!question && !image && !audio){
    status.innerText = "❌ Provide text, image or audio";
    return;
  }

  const fd = new FormData();
  if(question) fd.append("question", question);
  if(image) fd.append("image", image);
  if(audio) fd.append("audio", audio);

  status.innerText = "⏳ Processing...";
  answerBox.innerText = "";

  try{
    const res = await fetch("/ask", { method:"POST", body: fd });
    const data = await res.json();

    if(!res.ok){
      status.innerText = "❌ " + data.detail;
      return;
    }

    status.innerText = "✅ Done";

    let out = "";
    out += "Detected Text:\n" + data.detected_text + "\n\n";
    out += "Answer:\n" + data.answer + "\n\n";

    if(data.steps && data.steps.length){
      out += "Steps:\n";
      data.steps.forEach((s,i)=> out += (i+1)+". "+s+"\n");
      out += "\n";
    }

    out += "Agent Trace: " + data.agent_trace.join(" → ") + "\n";
    out += "Confidence: " + Math.round(data.confidence*100) + "%";

    answerBox.innerText = out;
  }
  catch(err){
    console.error(err);
    status.innerText = "❌ Backend unreachable";
  }
}

async function sendFeedback(isHelpful){
  await fetch("/feedback",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({ helpful: isHelpful })
  });
  alert("Thanks for your feedback!");
}