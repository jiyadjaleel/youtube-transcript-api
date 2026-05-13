from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Extract Video ID
        video_id = ""
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0][:11]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0][:11]
        
        if not video_id:
            return jsonify({"error": "Could not extract Video ID"}), 400

        # ROBUST TRANSCRIPT FETCHING
        try:
            # Try standard English first
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB'])
            full_transcript = " ".join([chunk['text'] for chunk in transcript_list])
            return jsonify({"transcript": full_transcript})
            
        except:
            # If standard English fails, ask the API for ALL available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Loop through them and just grab the very first one we find
            for transcript in transcript_list:
                transcript_data = transcript.fetch()
                full_transcript = " ".join([chunk['text'] for chunk in transcript_data])
                return jsonify({"transcript": full_transcript})
                
            # If the loop finishes and nothing was found
            return jsonify({"error": "Video has no closed captions available"}), 404

    except Exception as e:
        # Catch any weird catastrophic errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)