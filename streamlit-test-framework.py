import streamlit as st
import zipfile
import io
import textwrap




def get_framework_recommendation(answers):
    """
    Analyzes answers and returns framework recommendations
    """
    if answers['page_complexity'] == "Low" and answers['return_values'] == "No":
        return {
            "pattern": "Basic Page Object Model",
            "description": """
            Based on your responses, a Basic Page Object Model would be most suitable for your needs. This pattern is:
            - Simple to implement and maintain
            - Perfect for straightforward UI workflows
            - Easy to understand for new team members
            - Ideal for applications with minimal complexity
            """,
            "template_files": {
                "base_page.py": """
                from selenium.webdriver.support.wait import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                class BasePage:
                    def __init__(self, driver):
                        self.driver = driver
                        self.wait = WebDriverWait(driver, 10)
                    
                    def click_element(self, locator):
                        self.wait.until(EC.element_to_be_clickable(locator)).click()
                    
                    def enter_text(self, locator, text):
                        element = self.wait.until(EC.presence_of_element_located(locator))
                        element.clear()
                        element.send_keys(text)
                """,
                "login_page.py": """
                from selenium.webdriver.common.by import By
                from .base_page import BasePage

                class LoginPage(BasePage):
                    # Locators
                    USERNAME_INPUT = (By.ID, "username")
                    PASSWORD_INPUT = (By.ID, "password")
                    LOGIN_BUTTON = (By.ID, "login-btn")
                    
                    def login(self, username, password):
                        self.enter_text(self.USERNAME_INPUT, username)
                        self.enter_text(self.PASSWORD_INPUT, password)
                        self.click_element(self.LOGIN_BUTTON)
                """,
                "test_login.py": """
                import pytest
                from pages.login_page import LoginPage

                def test_successful_login(driver):
                    login_page = LoginPage(driver)
                    login_page.login("test_user", "password123")
                    # Add your assertions here
                """
            }
        }
    elif answers['return_values'] == "Yes" and answers['data_seeding'] == "Yes":
        return {
            "pattern": "Fluent Page Object Model",
            "description": """
            Based on your responses, a Fluent Page Object Model with data management would be most suitable. This pattern offers:
            - Method chaining for better readability
            - Integrated data management capabilities
            - Strong support for validation and assertions
            - Flexible test data handling
            """,
            "template_files": {
                "base_page.py": """
                from selenium.webdriver.support.wait import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                class BasePage:
                    def __init__(self, driver):
                        self.driver = driver
                        self.wait = WebDriverWait(driver, 10)
                    
                    def click_element(self, locator):
                        self.wait.until(EC.element_to_be_clickable(locator)).click()
                        return self
                    
                    def enter_text(self, locator, text):
                        element = self.wait.until(EC.presence_of_element_located(locator))
                        element.clear()
                        element.send_keys(text)
                        return self
                    
                    def get_element_text(self, locator):
                        return self.wait.until(EC.presence_of_element_located(locator)).text
                """,
                "data_manager.py": """
                import json
                from pathlib import Path

                class DataManager:
                    def __init__(self, data_path):
                        self.data_path = Path(data_path)
                    
                    def load_test_data(self, filename):
                        with open(self.data_path / filename) as f:
                            return json.load(f)
                    
                    def save_test_data(self, data, filename):
                        with open(self.data_path / filename, 'w') as f:
                            json.dump(data, f, indent=2)
                """
            }
        }
    else:
        return {
            "pattern": "Screened Page Object Model",
            "description": """
            Based on your responses, a Screened Page Object Model would work best. This pattern provides:
            - Clear separation of concerns
            - Robust error handling
            - Scalable architecture
            - Support for complex workflows
            """,
            "template_files": {
                "base_screen.py": """
                from selenium.webdriver.support.wait import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                class BaseScreen:
                    def __init__(self, driver):
                        self.driver = driver
                        self.wait = WebDriverWait(driver, 10)
                    
                    def perform_action(self, action_fn):
                        try:
                            return action_fn()
                        except Exception as e:
                            raise ScreenActionException(f"Action failed: {str(e)}")
                """,
                "login_screen.py": """
                from selenium.webdriver.common.by import By
                from .base_screen import BaseScreen

                class LoginScreen(BaseScreen):
                    def __init__(self, driver):
                        super().__init__(driver)
                        self.username_input = (By.ID, "username")
                        self.password_input = (By.ID, "password")
                    
                    def enter_credentials(self, username, password):
                        def _action():
                            self.enter_text(self.username_input, username)
                            self.enter_text(self.password_input, password)
                        return self.perform_action(_action)
                """
            }
        }

def create_download_link(files):
    """
    Creates a ZIP file containing the template files
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, textwrap.dedent(content).strip())
    return zip_buffer.getvalue()

def initialize_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {
            'return_values': None,
            'resource_limitation': None,
            'data_seeding': None,
            'multiple_platforms': None,
            'page_complexity': None
        }

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def update_answer(question, answer):
    st.session_state.answers[question] = answer

def main():
    st.title("Test Automation Framework Generator")
    st.write("Let's help you choose the right design pattern for your test automation framework.")
    
    initialize_session_state()
    
    # Create columns for the progress indicator
    total_steps = 5
    progress = (st.session_state.step - 1) / total_steps
    st.progress(progress)
    st.write(f"Step {st.session_state.step} of {total_steps}")
    
    if st.session_state.step == 1:
        st.subheader("Page Object Method Return Values")
        st.write("""When implementing page objects in your framework, do your test methods frequently need to return values 
                 for validation, such as getting element text, checking states, or retrieving data for assertions?""")
        
        st.write("📝 Common Scenarios:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Methods needing return values:**
            - Getting text from elements: `getErrorMessage()`, `getUsername()`
            - Validating element states: `isButtonEnabled()`, `isUserLoggedIn()`
            - Retrieving data for assertions: `getTableRowCount()`
            - Fetching form values: `getFormData()`, `getInputValue()`
            """)
        with col2:
            st.markdown("""
            **Methods without return values:**
            - Action methods: `clickLoginButton()`, `submitForm()`
            - Setup methods: `navigateToHome()`, `acceptCookies()`
            - Form filling: `enterUsername()`, `selectCountry()`
            - Multi-step processes: `completeCheckout()`
            """)
            
        answer = st.radio(
            "Select based on your framework's primary method types:",
            ["Yes - Most methods need to return values for validation and assertions",
             "No - Most methods are action-based without return values"],
            key="return_values_radio",
            index=0 if st.session_state.answers['return_values'] == "Yes" else 1 if st.session_state.answers['return_values'] == "No" else 0
        )
        update_answer('return_values', "Yes" if answer.startswith("Yes") else "No")

    elif st.session_state.step == 2:
        st.subheader("Test Execution Resource Management")
        st.write("""Does your testing environment have specific resource constraints that require careful management 
                 of test execution, such as limited device availability, license restrictions, or API rate limits?""")
        
        st.write("📝 Common Scenarios:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Resource-constrained environments:**
            - Limited device farm with shared mobile devices
            - CI/CD pipelines with concurrent execution limits
            - Licensed tools with user/session restrictions
            - Performance-sensitive environments
            - API testing with rate limiting
            """)
        with col2:
            st.markdown("""
            **Unrestricted environments:**
            - Local development machines
            - Unlimited cloud resources
            - Unit tests with mocks
            - Static code analysis
            - Simulation-based testing
            """)
            
        answer = st.radio(
            "Select based on your resource management needs:",
            ["Yes - Need to carefully manage and limit resource usage",
             "No - Resource management is not a significant concern"],
            key="resource_limitation_radio",
            index=0 if st.session_state.answers['resource_limitation'] == "Yes" else 1 if st.session_state.answers['resource_limitation'] == "No" else 0
        )
        update_answer('resource_limitation', "Yes" if answer.startswith("Yes") else "No")

    elif st.session_state.step == 3:
        st.subheader("Test Data Management Requirements")
        st.write("""Is your application heavily dependent on complex test data setup, requiring sophisticated fixture 
                 management or data seeding strategies for effective testing?""")
        
        st.write("📝 Common Scenarios:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Complex data requirements:**
            - E-commerce with product/order data
            - User management with role hierarchies
            - Multi-step approval workflows
            - Report generation with varied datasets
            - Cross-system integration testing
            """)
        with col2:
            st.markdown("""
            **Simple data requirements:**
            - Static content validation
            - UI/UX testing
            - Basic form validation
            - Authentication flows
            - Error handling scenarios
            """)
            
        answer = st.radio(
            "Select based on your test data complexity:",
            ["Yes - Complex test data setup is crucial for testing",
             "No - Minimal test data management is required"],
            key="data_seeding_radio",
            index=0 if st.session_state.answers['data_seeding'] == "Yes" else 1 if st.session_state.answers['data_seeding'] == "No" else 0
        )
        update_answer('data_seeding', "Yes" if answer.startswith("Yes") else "No")

    elif st.session_state.step == 4:
        st.subheader("Cross-Platform Testing Requirements")
        st.write("""Does your application need to be tested across multiple platforms, browsers, or devices, 
                 requiring a framework that can handle different environments and configurations?""")
        
        st.write("📝 Common Scenarios:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Multi-platform needs:**
            - Cross-browser web applications
            - iOS and Android mobile apps
            - Cross-OS desktop applications
            - Progressive Web Apps (PWAs)
            - Hybrid mobile/web applications
            """)
        with col2:
            st.markdown("""
            **Single platform needs:**
            - Web-only applications
            - Platform-specific tools
            - Single-platform mobile apps
            - API/backend services
            - Database applications
            """)
            
        answer = st.radio(
            "Select based on your platform coverage needs:",
            ["Yes - Need to test across multiple platforms/environments",
             "No - Testing focused on a single platform"],
            key="multiple_platforms_radio",
            index=0 if st.session_state.answers['multiple_platforms'] == "Yes" else 1 if st.session_state.answers['multiple_platforms'] == "No" else 0
        )
        update_answer('multiple_platforms', "Yes" if answer.startswith("Yes") else "No")

    elif st.session_state.step == 5:
        st.subheader("Page Object Complexity Assessment")
        st.write("""How sophisticated are your application's page objects in terms of interactive elements, 
                 dynamic content, and complex user workflows?""")
        
        st.write("📝 Common Scenarios:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **High complexity pages:**
            - Interactive dashboards
            - Rich content management systems
            - Complex financial calculators
            - Project management tools
            - Advanced e-commerce flows
            """)
        with col2:
            st.markdown("""
            **Low complexity pages:**
            - Basic login forms
            - Static content pages
            - Simple CRUD interfaces
            - Basic search functionality
            - User profile pages
            """)
            
        answer = st.radio(
            "Select based on your page object complexity:",
            ["High - Complex pages with many interactive elements and workflows",
             "Low - Simple pages with basic interactions and workflows"],
            key="page_complexity_radio",
            index=0 if st.session_state.answers['page_complexity'] == "High" else 1 if st.session_state.answers['page_complexity'] == "Low" else 0
        )
        update_answer('page_complexity', "High" if answer.startswith("High") else "Low")

    # Navigation buttons
    st.write("---")
    cols = st.columns(2)
    with cols[0]:
        if st.session_state.step > 1:
            st.button("← Previous", on_click=prev_step)
    with cols[1]:
        if st.session_state.step < total_steps:
            st.button("Next →", on_click=next_step)
        else:
            if st.button("Generate Framework"):
                st.write("---")
                st.subheader("🎯 Framework Recommendation")
                
                # Get recommendation based on answers
                recommendation = get_framework_recommendation(st.session_state.answers)
                
                # Display recommendation
                st.write("### " + recommendation["pattern"])
                st.write(recommendation["description"])
                
                # Create download link
                zip_file = create_download_link(recommendation["template_files"])
                
                st.write("### 📦 Download Boilerplate Code")
                st.write("""
                The download includes:
                - Base classes with core functionality
                - Example page objects/screens
                - Sample test cases
                - Utility functions
                """)
                
                st.download_button(
                    label="Download Framework Template",
                    data=zip_file,
                    file_name="test_framework_template.zip",
                    mime="application/zip",
                )
                
                st.write("### 📝 Next Steps")
                st.write("""
                1. Download and extract the template files
                2. Install required dependencies (selenium, pytest)
                3. Customize the base classes for your needs
                4. Create your page objects following the example structure
                5. Run the sample tests to verify the setup
                """)
                
                # Show all answers for reference
                st.write("### 🔍 Your Requirements Summary")
                st.json(st.session_state.answers)

if __name__ == "__main__":
    main()