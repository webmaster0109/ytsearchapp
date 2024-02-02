import streamlit as st
from youtubesearchpython import VideosSearch, PlaylistsSearch, Playlist
import time

def search_youtube_videos(query, max_limit=100):
    videos_search = VideosSearch(query, limit=max_limit)
    results = videos_search.result()
    return results["result"]

def search_youtube_playlist(playlist):
    playlistsSearch = PlaylistsSearch(playlist)
    playlists = playlistsSearch.result()
    return playlists["result"]

def get_playlist_videos(query):
    playlistVideos = Playlist.getVideos(query)
    return playlistVideos

def main():
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    # Sidebar menu
    sidebar_menu = st.sidebar.radio("Menu", ["Video Search", "Playlist Search", "Downloads", "Watchlist"])
    
    if sidebar_menu == "Video Search":
        st.title(f":rainbow[YouTube Video Search App]")
        # User input for video search
        query = st.text_input("Enter your Favorite YouTube Video:", "Solo Levelling Anime")

        # User input for results per page
        results_per_page = st.sidebar.selectbox("Results per Page", [5, 10, 15, 20, 50], index=2)

        start_time = time.time()
        # Get YouTube videos based on the search query
        videos = search_youtube_videos(query, max_limit=100)
        end_time = time.time()

        if videos:
            
            # Display the search results
            total_results = len(videos)
            # time.sleep(1)
            eclapsed_time_second = end_time - start_time
            st.markdown(
                f"<p style='font-size:16px;color:grey;'>About {total_results} results (in {eclapsed_time_second:.2f} seconds)</p>", 
                unsafe_allow_html=True
            )

            # Pagination controls
            current_page = st.sidebar.number_input("Page", min_value=1, value=1)
            total_pages = (total_results - 1) // results_per_page + 1

            start_idx = (current_page - 1) * results_per_page
            end_idx = min(start_idx + results_per_page, total_results)
            current_page_videos = videos[start_idx:end_idx]

            for video in current_page_videos:
                video_title = str(video['title'])
                st.markdown(f"## {video_title.upper()}")
                
                # video thumbnail
                thumbnail_url = video['thumbnails'][0]['url']
                st.image(thumbnail_url, use_column_width=True)

                with st.expander('Video Details:', expanded=True):
                    st.write(f"**Channel:** {video['channel']['name']}")
                    # Check if 'views' key is present in the video data
                    views = video['viewCount']
                    st.write(f"**Views:** {views['short']}")
                    
                    # Display video date using publishedText
                    published_text = video.get('publishedTime', 'N/A') if 'publishedTime' in video else 'N/A'
                    st.write(f"**Published Date:** {published_text}")
                    
                    st.write(f"**Duration:** {video['duration']}")

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
    
    elif sidebar_menu == "Playlist Search":
        st.title(f":rainbow[YT Playlist Search App]")
        # search playlist
        query = st.text_input("Search youtube playlist here: (*Type Anything)", "Krish Naik Hindi")
        # start time
        start_time = time.time()
        # store playlist function
        playlist = search_youtube_playlist(query)
        # end time
        end_time = time.time()

        if playlist:
            total_playlists = len(playlist)
            elapsed_time_seconds = end_time - start_time
            st.markdown(
                f"<p style='font-size:16px;color:grey;'>About {total_playlists} results (in {elapsed_time_seconds:.2f} seconds)</p>", 
                unsafe_allow_html=True
            )

            for video in playlist:
                video_title = str(video['title'])
                st.markdown(f"### {video_title.upper()}")

                thumbnail_url = video['thumbnails'][2]['url']
                st.image(thumbnail_url, use_column_width=True)

                with st.expander('Playlist Details:', expanded=True):
                    st.write(f"**Channel:** {video['channel']['name']}")
                    # Check if 'views' key is present in the video data
                    st.write(f"**Total Videos:** {video['videoCount']}")

                with st.expander(f'{video["title"]}'):
                    if st.button("Show Videos: ", key=f"playlist_videos_{video['title']}"):
                        start_time = time.time()
                        playlist_videos = get_playlist_videos(video['link'])['videos']
                        end_time = time.time()
                        elapsed_time_seconds = end_time - start_time

                        if playlist_videos:
                            st.markdown(
                                f"<p style='font-size:16px;color:grey;'>About {len(playlist_videos)} results (in {elapsed_time_seconds:.2f} seconds)</p>", 
                                    unsafe_allow_html=True
                            )
                            for pv in playlist_videos:
                                st.markdown(f"##### {pv['title']}")
                                st.write(f"**Duration:** {pv['duration']}")

                                video_embed_code = f'<iframe width="100%" height="380" src="https://www.youtube.com/embed/{pv["id"]}" frameborder="0" allowfullscreen></iframe>'
                                st.markdown(video_embed_code, unsafe_allow_html=True)
                                st.write("----")

                st.write("----")

    elif sidebar_menu == "Watchlist":
        st.title(f":rainbow[YouTube Video Watchlist]")
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
