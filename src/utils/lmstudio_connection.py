import requests


def query_lmstudio(context, user_query, max_tokens=300):
    """Query LMStudio for completion"""
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    prompt = f"""Based on the following context, please answer the question. If the answer cannot be found in the context, say so.

    Context:
    {context}
    
    Question: {user_query}
    
    Answer:"""

    payload = {
        "model": "phi-4",
        "messages": [
            {"role": "system",
             "content": "You are a helpful AI assistant that answers questions based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LMStudio: {str(e)}"

context = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum., my name is yashaswa, Diam per scelerisque nullam hendrerit est suspendisse. Gravida orci at ridiculus ex aliquam sem consequat viverra! Eleifend augue mi consectetur quam at proin sit. Ligula senectus efficitur ex magnis, id mattis. Sociosqu orci orci habitant euismod himenaeos pellentesque. Elit ipsum metus sem malesuada finibus mus sapien? Pharetra magna maximus magna consectetur lorem potenti sociosqu. Vitae lacinia duis commodo magnis morbi phasellus accumsan neque. Justo scelerisque et quisque tellus dictum."
user_query = "what is my pet's name??"
lms_result = query_lmstudio(context=context, user_query = user_query)
print(lms_result)