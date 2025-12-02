import streamlit as st
import json
from pathlib import Path

def render_tab(PROJECT_ROOT: Path):
    """Renders the content for Tab 11: Bulletin Board."""
    st.header("📌 게시판")

    BOARD_PATH = PROJECT_ROOT / "board.json"

    # Create board file if it doesn't exist
    if not BOARD_PATH.exists():
        with open(BOARD_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    # Load board data
    with open(BOARD_PATH, "r", encoding="utf-8") as f:
        board_data = json.load(f)

    # --- Write Post ---
    st.subheader("✏ 게시글 작성")
    with st.form("new_post_form", clear_on_submit=True):
        title = st.text_input("제목")
        content = st.text_area("내용")
        submitted = st.form_submit_button("📝 글 저장")

        if submitted:
            if not title or not content:
                st.warning("제목과 내용을 모두 입력해주세요.")
            else:
                new_post = {"title": title, "content": content}
                board_data.append(new_post)
                with open(BOARD_PATH, "w", encoding="utf-8") as f:
                    json.dump(board_data, f, ensure_ascii=False, indent=4)
                st.success("📌 글이 저장되었습니다!")
                # No st.rerun() needed here, form clears on submit and board will be re-read on next interaction

    st.markdown("---")

    # --- Post List ---
    st.subheader("📚 게시글 목록")

    if not board_data:
        st.info("아직 작성된 글이 없습니다.")
    else:
        # Display latest posts first
        reversed_board_data = list(reversed(board_data))
        
        for idx, post in enumerate(reversed_board_data):
            with st.expander(f"**{post['title']}**"):
                st.write(post["content"])
                
                # Delete button for each post
                if st.button("🗑️ 이 글 삭제하기", key=f"delete_{idx}"):
                    # Find the post in the original (non-reversed) list and remove it
                    # This is safe because post objects are unique dictionaries
                    board_data.remove(post)
                    
                    # Save the updated data
                    with open(BOARD_PATH, "w", encoding="utf-8") as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=4)
                    
                    st.success(f"'{post['title']}' 글이 삭제되었습니다!")
                    st.rerun()
