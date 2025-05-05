# Display tariff information if it has been applied
                if st.session_state.tariff_applied:
                    tariffed_cost = st.session_state.result['Cost'] * 1.25  # Adding 25% tariff
                    latest_design = st.session_state.car_designs[-1]
                    tariffed_profit = st.session_state.result['Estimated Sales'] * (latest_design['Price'] - tariffed_cost)
                    tariffed_feedback = get_feedback_for_profit(tariffed_profit, st.session_state.result['Estimated Sales'])
                    
                    st.markdown(f"""
                    <div class="custom-container-tariff">
                        <h2 class="header-orange">Updated Market Results (After Tariff)</h2>
                        <p><strong>Best Market Segment:</strong> {st.session_state.result['Best Market Segment']}</p>
                        <p><strong>Estimated Sales:</strong> {st.session_state.result['Estimated Sales']} units</p>
                        <p><strong>Original Profit:</strong> ${st.session_state.result['Profit']:,}</p>
                        <p><strong>New Estimated Profit:</strong> ${tariffed_profit:,.2f}</p>
                        <p><strong>Profit Change:</strong> ${tariffed_profit - st.session_state.result['Profit']:,.2f}</p>
                        <div class="section-divider">
                            <h3 class="header-orange">Updated Profit Feedback</h3>
                            <p>{tariffed_feedback}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Game over summary at the end
                if st.session_state.game_state == "game_over":
                    # Calculate best attempt
                    profits = [result['Profit'] for result in st.session_state.attempts_results]
                    best_attempt_index = profits.index(max(profits))
                    best_attempt = st.session_state.attempts_results[best_attempt_index]
                    best_design = st.session_state.car_designs[best_attempt_index]
                    
                    st.markdown("""
                    <div class="section-divider"></div>
                    <h2 style="text-align: center; margin-top: 20px;">Game Summary</h2>
                    """, unsafe_allow_html=True)
                    
                    # Best design callout
                    st.markdown(f"""
                    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 2px solid #3498db; margin-bottom: 20px;">
                        <h3 style="color: #3498db; text-align: center;">Best Performing Design: Attempt {best_attempt_index+1}</h3>
                        <p><strong>Profit:</strong> ${best_attempt['Profit']:,}</p>
                        <p><strong>Market Segment:</strong> {best_attempt['Best Market Segment']}</p>
                        <p><strong>Settings:</strong> Speed: {best_design['Speed']}, Aesthetics: {best_design['Aesthetics']}, 
                        Reliability: {best_design['Reliability']}, Efficiency: {best_design['Efficiency']}, 
                        Tech: {best_design['Tech']}, Price: ${best_design['Price']:,}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a DataFrame for the summary
                    import pandas as pd
                    summary_data = []
                    for i, (design, result) in enumerate(zip(st.session_state.car_designs, st.session_state.attempts_results)):
                        is_best = i == best_attempt_index
                        best_badge = "Best " if is_best else ""
                        summary_data.append({
                            "Attempt": f"{best_badge}Attempt {i+1}",
                            "Market Segment": result['Best Market Segment'],
                            "Sales": result['Estimated Sales'],
                            "Profit": f"${result['Profit']:,}",
                            "Speed": design['Speed'],
                            "Aesthetics": design['Aesthetics'],
                            "Reliability": design['Reliability'],
                            "Efficiency": design['Efficiency'],
                            "Tech": design['Tech'],
                            "Price": f"${design['Price']:,}"
                        })
                    
                    summary_df = pd.DataFrame(summary_data)
                    
                    # Display the summary table
                    st.markdown("### All Attempts Comparison")
                    st.dataframe(summary_df, use_container_width=True)
                    
                    # Educational message about relevant courses
                    st.markdown("""
                    <div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #1890ff; margin: 20px 0;">
                        <h3 style="color: #1890ff; margin-top: 0;">Educational Note</h3>
                        <p>Taking courses at Coast Mountain College such as <strong>Introduction to Marketing</strong> and <strong>Business Finance</strong> would help you understand markets and how to price products accordingly!</p>
                        <p>Interested in more information? Visit the <a href="https://coastmountaincollege.ca/programs/study/business" target="_blank">Coast Mountain College Business Administration website</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tariff button after 3rd attempt if not already applied
                    col1, col2 = st.columns(2)
                    with col1:
                        if not st.session_state.tariff_applied:
                            # Fix for tariff button disappearing
                            tariff_button = st.button(
                                "Impose Trump Tariff +25%", 
                                key="apply_tariff",
                                type="secondary"
                            )
                            if tariff_button:
                                st.session_state.tariff_applied = True
                                st.rerun()
                    
                    with col2:
                        # New game button
                        if st.button("Start New Game", key="new_game_button", type="primary"):
                            reset_game()
                            st.rerun()
            
            except Exception as e:
                st.error(f"Error displaying results: {str(e)}")
                # Add a debug expander
                with st.expander("Debug Information"):
                    st.write("Debug Info:", st.session_state.debug_info)
                    st.write("Error:", str(e))
                    st.write("Error Type:", type(e).__name__)
                    import traceback
                    st.write("Traceback:", traceback.format_exc())
        
        # Show a placeholder message if no results to display yet
        else:
            st.markdown("""
            <div style="text-align: center; padding: 30px; background-color: #f5f5f5; border-radius: 10px;">
                <h3>Your results will appear here</h3>
                <p>Adjust the car settings on the left and click "Simulate Market" to see how your design performs.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# Add a hidden debug expander at the bottom for developer troubleshooting
with st.expander("Developer Debug", expanded=False):
    st.write("### Debug Information")
    st.write("Game State:", st.session_state.game_state)
    st.write("Attempts Used:", st.session_state.attempts_used)
    st.write("Debug Log:", st.session_state.debug_info)
    
    # API Key status check
    if hasattr(st, 'secrets') and 'openai_api_key' in st.secrets:
        st.write("API Key in Secrets: Yes")
    else:
        st.write("API Key in Secrets: No")
        
    if os.getenv("OPENAI_API_KEY"):
        st.write("API Key in Environment: Yes")
    else:
        st.write("API Key in Environment: No")
    
    # Check Car Image URL
    if st.session_state.car_image_url:
        st.write("Car Image URL:", st.session_state.car_image_url[:50] + "..." if len(st.session_state.car_image_url) > 50 else st.session_state.car_image_url)
    
    # Add a manual refresh button for debugging
    if st.button("Manual Refresh", key="debug_refresh"):
        st.rerun()
