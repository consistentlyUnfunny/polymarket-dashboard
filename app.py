import streamlit as st
import pandas as pd
from src.clients.gamma import GammaClient
from src.core.filters import filter_candidates
from src.core.select_focus import select_focus_markets
from src.clients.clob import ClobClient

# page config
st.set_page_config(
    page_title="Polymarket Dashboard",
    layout="wide"
)

@st.cache_data(ttl=60) # Cache data for 60 seconds
def load_data():
    # fetch parse and filter data from the api
    gamma_client = GammaClient()
    clob_client = ClobClient()
    
    # Fetch raw data (5 pages = 500 items)
    raw_markets = gamma_client.fetch_markets(pages=5)

    # for debugging: print how many samples found
    print(f"DEBUG: Fetched {len(raw_markets)} raw markets from API.")
    if len(raw_markets) > 0:
        sample = raw_markets[0]
        print(f"DEBUG: Sample Market -> Active: {sample.active}, Closed: {sample.closed}, Book: {sample.enable_order_book}, Hours: {sample.hours_to_close}, Invalid: {sample.invalid_reason}")


    # 2. Filter
    candidates = filter_candidates(raw_markets)
    print(f"DEBUG: {len(candidates)} candidates remained after filtering.")

    candidates = filter_candidates(raw_markets)
    all_token_ids = []
    for m in candidates:
        if m.yes_token_id: all_token_ids.append(m.yes_token_id)
        if m.no_token_id: all_token_ids.append(m.no_token_id)
        
    # fetch prices by batches
    if all_token_ids:
        live_prices = clob_client.get_prices(all_token_ids)
        
        # Update market records with new prices
        for m in candidates:
            if m.yes_token_id in live_prices:
                m.yes_price = live_prices[m.yes_token_id]

            if m.no_token_id in live_prices:
                m.no_price = live_prices[m.no_token_id]

    # Select Focus
    crypto, sports = select_focus_markets(candidates)
    
    return candidates, crypto, sports

def main():
    #header
    st.title("Polymarket Opportunities")
    st.markdown("Monitor active Yes/No markets closing within **48 hours**.")

    # Loading State
    with st.spinner('Fetching live market data...'):
        candidates, crypto_pick, sports_pick = load_data()

    st.divider()

    # Focus Section
    st.subheader("Focus Markets")
    
    # display focus side by side
    col1, col2 = st.columns(2)

    # Helper func to display a market card 
    def display_market_card(column, title, market):
        with column:
            st.markdown(f"### {title}")
            if market:
                st.info(market.question)
                # Nested columns for stats
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Yes Price", f"${market.yes_price}" if market.yes_price else "N/A")
                m_col2.metric("No Price", f"${market.no_price}" if market.no_price else "N/A")
                m_col3.metric("Closing In", f"{market.hours_to_close}h")
                st.caption(f"ID: {market.id}")
            else:
                st.warning("No suitable market found in current batch.")

    display_market_card(col1, "Crypto Pick", crypto_pick)
    display_market_card(col2, "Sports Pick", sports_pick)

    st.divider()

    # table
    st.subheader(f"📋 Candidate List ({len(candidates)} markets)")

    # one click filter button
    hide_invalid_prices = st.toggle("Filter: Hide rows with missing prices", value=False)

    if not candidates:
        st.write("No active candidates found.")
        return

    # Convert objects to a pd.dataframe for the table
    df = pd.DataFrame([vars(m) for m in candidates])

    # create full url by adding the Polymarket domain to the slug
    df["url"] = "https://polymarket.com/event/" + df["slug"]
    
    display_cols = [
        "category", "question", "end_date_iso", 
        "hours_to_close", "yes_price", "no_price", "url"
    ]
    
    # Apply button filter logic
    if hide_invalid_prices:
        # Drop Nan or None rows
        df = df.dropna(subset=['yes_price', 'no_price'])

    # display the model
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "yes_price": st.column_config.NumberColumn("Yes ($)", format="$%.2f"),
            "no_price": st.column_config.NumberColumn("No ($)", format="$%.2f"),
            "hours_to_close": st.column_config.NumberColumn("Hours Left", format="%.1f h"),
            
            "url": st.column_config.LinkColumn("Link", display_text="Open")
        }
    )


if __name__ == "__main__":
    main()