import streamlit as st
from youtubesearchpython import VideosSearch

def search_youtube_videos(query, max_results=50):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    return results["result"]

def main():
    st.markdown(f"# :rainbow[YouTube Video Search App]")

    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    # Sidebar menu
    sidebar_menu = st.sidebar.radio("Menu", ["Search", "Downloads", "Watchlist"])
    
    if sidebar_menu == "Search":
        # User input for video search
        query = st.text_input("Enter your Favorite YouTube Video:", "Solo Levelling Anime")

        # User input for results per page
        results_per_page = st.sidebar.selectbox("Results per Page", [5, 10, 15, 20, 50], index=2)

        # Get YouTube videos based on the search query
        videos = search_youtube_videos(query, max_results=50)

        if videos:
            # Display the search results with pagination
            total_results = len(videos)
            st.write(f"Total Results: {total_results}")

            # Pagination controls
            current_page = st.sidebar.number_input("Page", min_value=1, value=1)
            total_pages = (total_results - 1) // results_per_page + 1

            start_idx = (current_page - 1) * results_per_page
            end_idx = min(start_idx + results_per_page, total_results)
            current_page_videos = videos[start_idx:end_idx]

            for video in current_page_videos:
                st.markdown(f"### {video['title']}")
                st.write(f"**Channel:** {video['channel']['name']}")
                
                # Check if 'views' key is present in the video data
                views = video.get('views', 'N/A') if 'views' in video else 'N/A'
                st.write(f"**Views:** {views}")
                
                # Display video date using publishedText
                published_text = video.get('publishedTime', 'N/A') if 'publishedTime' in video else 'N/A'
                st.write(f"**Published Date:** {published_text}")
                
                st.write(f"**Duration:** {video['duration']}")
                thumbnail_url = video['thumbnails'][0]['url']
                st.image(thumbnail_url, use_column_width=True)

                # Add a clickable thumbnail that opens a pop-up
                with st.expander("Watch Video"):
                    video_embed_code = f'<iframe width="100%" height="380" src="https://www.youtube.com/embed/{video["id"]}" frameborder="0" allowfullscreen></iframe>'
                    st.markdown(video_embed_code, unsafe_allow_html=True)
                    
                    if st.button(f"Add to Watchlist", key=f"watchlist_{video['id']}"):
                        # Add the selected video to the watchlist along with its link
                        st.session_state.watchlist.append({"title": video['title'], "link": f"https://www.youtube.com/watch?v={video['id']}"})
                        st.success(f"Added '{video['title']}' to watchlist.")

                st.write("----")

            # Pagination controls
            if total_pages > 1:
                st.sidebar.markdown(f"Page {current_page} of {total_pages}")
                previous_page = st.sidebar.button("Previous Page", key="prev_page", disabled=current_page == 1)
                next_page = st.sidebar.button("Next Page", key="next_page", disabled=current_page == total_pages)

                if previous_page:
                    current_page -= 1

                if next_page:
                    current_page += 1

        else:
            st.warning("No videos found. Try a different search query.")
    
    elif sidebar_menu == "Watchlist":
        st.write("Watchlist menu selected.")
        watchlist = st.session_state.watchlist
        if not watchlist:
            st.warning("Your watchlist is empty.")
        else:            
            for video in watchlist:
                st.markdown(f"### {video['title']}")
                link = str(video['link']).split('=')[1]
                with st.expander("Watch Video"):
                    video_embed_code = f'<iframe width="100%" height="380" src="https://www.youtube.com/embed/{link}" frameborder="0" allowfullscreen></iframe>'
                    st.markdown(video_embed_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
