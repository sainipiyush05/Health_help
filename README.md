# 🛒 Project 10: AI Shopping Assistant

An intelligent, conversational AI Shopping Assistant powered by **LangChain** and **Groq LLMs**. It enables users to search for products, view ratings, and place orders using either natural language text queries or by uploading a product image (multimodal search).

---

## 🌟 Key Features

1. **Natural Language Shopping:** Search, filter by price, and filter by organic status simply by chatting with the assistant (e.g., *"I want organic honey under $20 with a 4.5+ rating"*).
2. **Visual Product Search (Multimodal):** Upload a product image (e.g., honey jar, oats packaging) via the sidebar. The assistant uses a vision model to analyze the image, extract attributes, and query the store database for matching products.
3. **Product Rating & Reviews Integration:** Automatically retrieves customer ratings and review statistics for products to help you make informed decisions.
4. **Interactive Ordering Workflow:** Place an order securely. The assistant will guide you through the process, ask for confirmation, and update the database with order details upon successful checkout.
5. **Interactive UI:** Interactive Streamlit web interface with conversational history, real-time message streaming, and a sidebar for image upload.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    User([User]) <--> App[Streamlit Web App: app.py]
    App <--> Agent[LangChain Agent: shopping_agent.py]
    
    subgraph LLM Services (Groq)
        LLM[ChatGroq: qwen/qwen3-32b]
        VisionLLM[ChatGroq: meta-llama/llama-4-scout-17b-16e-instruct]
    end
    
    Agent -->|Main Chat| LLM
    Agent -->|Image Description| VisionLLM
    
    subgraph Tools
        T1[search_products]
        T2[get_rating]
        T3[checkout]
        T4[describe_product_image]
    end
    
    Agent --> Tools
    
    T1 -->|Query Products| DB[(SQLite Database: store.db)]
    T2 -->|Retrieve Ratings| API[Reviews API: reviews_api.py]
    API -->|Fetch Reviews| DB
    T3 -->|Place Order| DB
```

### File Structure & Roles
- [app.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/10_project_shopping_agent/app.py): The main Streamlit web application. Handles message history, sidebar image uploads, and session state.
- [shopping_agent.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/10_project_shopping_agent/shopping_agent.py): Defines the LangChain agent, system prompt rules, and the tools:
  - `search_products`: Searches SQLite database with criteria.
  - `get_rating`: Queries reviews database for average rating and counts.
  - `checkout`: Places an order and records it in SQLite.
  - `describe_product_image`: Multimodal tool utilizing base64 encoding and vision LLM.
- [reviews_api.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/10_project_shopping_agent/reviews_api.py): Provides aggregated rating info from the `reviews` table.
- [setup_db.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/10_project_shopping_agent/setup_db.py): Database initialization script containing sample products and seed review comments.
- [resources/](file:///Users/piyushsaini/Desktop/AI/learn_agentic/10_project_shopping_agent/resources): Contains sample product images (`honey.png`, `oats.png`) that can be used to test the sidebar image-search functionality.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Make sure you have python installed (Python 3.10+ recommended) and the required packages. Ensure your virtual environment is active.

### 2. Configure Environment Variables
Create a `.env` file in the root workspace directory (if not already done) and provide your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Initialize the Database
Populate the local SQLite database (`store.db`) with test products and reviews by running the setup script:
```bash
python setup_db.py
```
This will create a `store.db` file containing:
- **32 Products** across categories: honey, oil, nuts, seeds, grains, tea, coffee, snacks, and dairy alternatives.
- **Over 100 mock customer reviews** with diverse ratings.
- An empty **Orders** table to record purchases.

---

## 🚀 Running the Application

Start the Streamlit user interface:
```bash
streamlit run app.py
```
This will launch the app in your browser (usually at `http://localhost:8501`).

### How to Test
1. **Text Search:** Ask: *"I'm looking for organic green tea. Show me options with a rating above 4.5 and under $15."*
2. **Image Search:** Upload one of the test images (e.g. `10_project_shopping_agent/resources/honey.png`) from the sidebar. Click **Find similar products**.
3. **Ordering:** When the assistant presents a product list, confirm the order by replying: *"Yes, place an order for the first one"* or *"Order #1"*.
