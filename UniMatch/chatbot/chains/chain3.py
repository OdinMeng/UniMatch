# Import necessary libraries and modules
import json
from typing import List, Optional

from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from pydantic import BaseModel, Field

from company_name.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from company_name.data.loader import load_database_file

# Define the product database as a dictionary with product categories
PRODUCT_DATABASE = {
    "Computers and Laptops": [
        "TechPro Ultrabook",
        "BlueWave Gaming Laptop",
        "PowerLite Convertible",
        "TechPro Desktop",
        "BlueWave Chromebook",
    ],
    "Smartphones and Accessories": [
        "SmartX ProPhone",
        "MobiTech PowerCase",
        "SmartX MiniPhone",
        "MobiTech Wireless Charger",
        "SmartX EarBuds",
    ],
    "Televisions and Home Theater Systems": [
        "CineView 4K TV",
        "SoundMax Home Theater",
        "CineView 8K TV",
        "SoundMax Soundbar",
        "CineView OLED TV",
    ],
    "Gaming Consoles and Accessories": [
        "GameSphere X",
        "ProGamer Controller",
        "GameSphere Y",
        "ProGamer Racing Wheel",
        "GameSphere VR Headset",
    ],
    "Audio Equipment": [
        "AudioPhonic Noise-Canceling Headphones",
        "WaveSound Bluetooth Speaker",
        "AudioPhonic True Wireless Earbuds",
        "WaveSound Soundbar",
        "AudioPhonic Turntable",
    ],
    "Cameras and Camcorders": [
        "FotoSnap DSLR Camera",
        "ActionCam 4K",
        "FotoSnap Mirrorless Camera",
        "ZoomMaster Camcorder",
        "FotoSnap Instant Camera",
    ],
}


# Base Models for data handling using Pydantic
class ProductCategory(BaseModel):
    """Model for representing a product category and its products."""

    category: Optional[str] = Field(None, description="The product category")
    products: Optional[List[str]] = Field(
        None, description="List of products mentioned"
    )


class ProductQueryResult(BaseModel):
    """Model for the result containing multiple product categories."""

    results: List[ProductCategory]


# Product Information Reasoning Chain - Uses a language model (LLM) to process product info
class ReasoningChain3(Runnable):
    """Chain that processes product information reasoning from a customer query."""

    def __init__(self, llm, memory=False):
        """Initialize the product info reasoning chain."""
        super().__init__()
        self.product_database = PRODUCT_DATABASE
        self.categories, self.products = self._format_product_database()
        self.llm = llm
        self.products_catalog = load_database_file("products_catalog.pkl")

        # Define the prompt template for product identification
        prompt_template = PromptTemplate(
            system_template="""
            You are a product identification system for an electronics store.
            Your task is to analyze customer service queries and identify mentioned products and categories.

            Available categories:
            {categories}

            Available products:
            {products}

            {format_instructions}

            Ensure your response follows the exact format specified in the instructions.
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)
        self.output_parser = PydanticOutputParser(pydantic_object=ProductQueryResult)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.chain = (self.prompt | self.llm | self.output_parser).with_config(
            {"run_name": self.__class__.__name__}
        )  # Add a run name to the chain on LangSmith

    def _format_product_database(self):
        """Format the product database into strings for categories and products."""
        categories = "\n".join(
            f"- {category}" for category in self.product_database.keys()
        )
        products = "\n".join(
            f"{category}:\n" + "\n".join(f"  - {product}" for product in products)
            for category, products in self.product_database.items()
        )
        return categories, products

    def _get_product_by_name(self, name):
        """Retrieve a product from the catalog by its name."""
        return self.products_catalog.get(name, None)

    def _get_products_by_category(self, category):
        """Retrieve a list of products that belong to a specific category."""
        return [
            product
            for product in self.products_catalog.values()
            if product["category"] == category
        ]

    def _generate_output_string(self, data_list):
        """Generate a formatted string output from a list of ProductCategory objects."""
        output_string = ""

        if data_list is None:
            return output_string

        for data in data_list:
            try:
                # Check if the data is an instance of ProductCategory
                if isinstance(data, ProductCategory):

                    # Process category-based product data
                    if data.category:
                        category_products = self._get_products_by_category(
                            data.category
                        )
                        for product in category_products:
                            output_string += json.dumps(product, indent=4) + "\n"

                    # Process product-based data
                    if data.products:
                        for product_name in data.products:
                            product = self._get_product_by_name(product_name)
                            if product:
                                output_string += json.dumps(product, indent=4) + "\n"
                            else:
                                print(f"Error: Product '{product_name}' not found")
                else:
                    print("Error: Invalid object format")
            except Exception as e:
                print(f"Error: {e}")

        return output_string

    def invoke(self, inputs) -> str:
        with callbacks.collect_runs() as cb:
            """Invoke the product information reasoning chain."""
            response = self.chain.invoke(
                {
                    "customer_input": inputs["customer_input"],
                    "categories": self.categories,
                    "products": self.products,
                    "format_instructions": self.format_instructions,
                }
            )

            # Generate and return the product information output
            inputs["product_info"] = self._generate_output_string(response.results)
            return inputs


# Customer Service Response Chain - Uses a language model (LLM) to generate customer service responses
class ResponseChain3(Runnable):
    """Chain that generates a response to customer queries about products."""

    def __init__(self, llm, memory=True):
        """Initialize the product information response chain."""
        super().__init__()
        self.llm = llm

        # Define the prompt template for customer service interaction
        prompt_template = PromptTemplate(
            system_template="""
            You are a friendly and helpful customer service assistant for a large electronics store.
            Follow these guidelines:
            1. Provide concise, helpful responses
            2. Ask relevant follow-up questions when needed
            3. Show understanding of specific products mentioned
            4. Be professional but conversational in tone
            5. Focus on solving the customer's immediate needs
            """,
            human_template="""
            Product Information from Query:
            {product_info}

            Customer Query: {customer_input}
            """,
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)

        # Chain to combine the prompt with LLM processing
        self.chain = self.prompt | self.llm

    def invoke(self, inputs, config):
        with callbacks.collect_runs() as cb:
            """Invoke the product information response chain."""
            return self.chain.invoke(inputs, config=config)
