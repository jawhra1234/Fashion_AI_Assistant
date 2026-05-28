import streamlit as st
import requests
from PIL import Image
import io

# Backend API URL
BACKEND_URL = "http://localhost:8000/recommend"

st.title("Agentic AI Fashion Assistant")
st.markdown("Get personalized outfit recommendations powered by AI!")

# Input section
st.header("Input Your Details")

# Occasion input
occasion = st.text_input(
    "Occasion",
    placeholder="e.g., casual, formal, business casual, summer party",
    help="Describe the occasion for your outfit"
)

# Image upload
uploaded_file = st.file_uploader(
    "Upload an image of your clothing (optional)",
    type=["jpg", "jpeg", "png"],
    help="Upload a photo of the clothing item you want to style"
)

# Recommendation button
if st.button("Get Recommendation", type="primary"):
    if not occasion:
        st.error("Please enter an occasion!")
    else:
        with st.spinner("Analyzing your request..."):
            try:
                # Prepare data for API
                files = {}
                data = {"occasion": occasion}
                
                if uploaded_file is not None:
                    # Convert uploaded file to bytes
                    image_bytes = uploaded_file.getvalue()
                    files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
                
                # Make API request
                if files:
                    response = requests.post(BACKEND_URL, data=data, files=files)
                else:
                    response = requests.post(BACKEND_URL, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("Recommendation generated!")
                    
                    # Show uploaded image if provided
                    if uploaded_file is not None:
                        st.header("📸 Uploaded Image")
                        st.image(uploaded_file, caption="Your uploaded clothing", use_container_width=True)
                    
                    # Show detected items if available
                    detected_items = result.get("detected_items")
                    if detected_items:
                        st.header("🧾 Detected Clothing Items")
                        for item in detected_items:
                            st.write(f"• {item}")
                    
                    # Outfit
                    st.header("👗 Recommended Outfit")
                    outfit_items = result.get("outfit", [])
                    if outfit_items:
                        for item in outfit_items:
                            st.write(f"• {item}")
                    else:
                        st.write("No outfit recommendations available.")
                    
                    # Reasoning
                    st.header("💭 Reasoning")
                    reasoning = result.get("reasoning", "No reasoning provided")
                    st.write(reasoning)
                    
                    # Style Score
                    score = result.get("style_score", 0)
                    st.header("⭐ Style Score")
                    st.metric("Score", f"{score}/10")
                    
                    # Alternative
                    st.header("🔄 Alternative Option")
                    alternative = result.get("alternative", [])
                    if alternative:
                        for alt in alternative:
                            st.write(f"• {alt}")
                    else:
                        st.write("No alternative provided.")
                
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
                st.info("Make sure the backend is running on http://localhost:8000")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using FastAPI, Streamlit, and open-source AI models")