import streamlit as st
from youtubesearchpython import VideosSearch

def search_youtube_videos(query, max_results=20):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    return results["result"]

def display_videos(videos, page_size=5):
    total_results = len(videos)
    st.write(f"Total Results: {total_results}")

    # Pagination controls
    current_page = st.sidebar.number_input("Page", min_value=1, value=1)
    total_pages = (total_results - 1) // page_size + 1

    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_results)
    current_page_videos = videos[start_idx:end_idx]

    for video in current_page_videos:
        st.markdown(f"### {video['title']}")
        st.write(f"**Channel:** {video['channel']['name']}")
        
        # Check if 'views' key is present in the video data
        views = video.get('views', 'N/A') if 'views' in video else 'N/A'
        st.write(f"**Views:** {views}")
        st.write(f"**Duration:** {video['duration']}")
        thumbnail_url = video['thumbnails'][0]['url']
        st.image(thumbnail_url, use_column_width=True)
        
        # Add a clickable thumbnail that opens a pop-up
        with st.expander("Watch Video"):
            video_embed_code = f'<iframe width="100%" height="280" src="https://www.youtube.com/embed/{video["id"]}" frameborder="0" allowfullscreen></iframe>'
            st.markdown(video_embed_code, unsafe_allow_html=True)

        st.write("----")

    # Pagination controls
    if total_pages > 1:
        st.sidebar.markdown(f"Page {current_page} of {total_pages}")
        previous_page = st.sidebar.button("Previous Page", key="prev_page", disabled=current_page == 1)
        next_page = st.sidebar.button("Next Page", key="next_page", disabled=current_page == total_pages)

        if previous_page:
            st.experimental_rerun()

        if next_page:
            st.experimental_rerun()

# Streamlit app
def main():
    st.title("YouTube Video Search App")

    # User input for video search
    query = st.text_input("Enter your YouTube video search query:", "Python tutorial")

    # User input for results per page
    results_per_page = st.sidebar.selectbox("Results per Page", [5, 10, 15, 20], index=2)

    if st.button("Search"):
        # Get YouTube videos based on the search query
        videos = search_youtube_videos(query, max_results=20)

        if videos:
            # Display the search results with pagination
            display_videos(videos, page_size=results_per_page)
        else:
            st.warning("No videos found. Try a different search query.")

if __name__ == "__main__":
    main()
