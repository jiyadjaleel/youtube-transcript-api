from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Extract the 11-character video ID from standard or shortened links
        video_id = ""
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0][:11]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0][:11]
        
        if not video_id:
            return jsonify({"error": "Could not extract Video ID"}), 400

        # Fetch the transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all the text chunks into one massive string
        full_transcript = " ".join([chunk['text'] for chunk in transcript_list])
        
        return jsonify({"transcript": full_transcript})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)