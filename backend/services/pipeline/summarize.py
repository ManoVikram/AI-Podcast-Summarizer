import ollama

def summarize_text(transcript):
    # Step 1 - Construct the prompt for summarization
    prompt = f"""
        Summarize the podcast transcript.

        Return exactly:
        1) A list of concise bullet points
        2) One short paragraph summary

        Transcript:
        {transcript}
        """
    
    # Step 2 - Call the Ollama API to get the summary
    response = ollama.chat(
        model="llama2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes podcast transcripts."},
            {"role": "user", "content": prompt}
        ]
    )
    text = response["message"]["content"]

    # Step 3 - Extract the bullet points from the response text
    bullet_points = [line.strip("- ").strip() for line in text.split("\n") if line.startswith("- ")]

    # Step 4 - Extract the summary paragraph from the response text
    paragraph_lines = [line.strip() for line in text.split("\n") if line.strip() != "" and not line.strip().startswith("- ")]
    summary_paragraph = " ".join(paragraph_lines).strip()

    return bullet_points, summary_paragraph