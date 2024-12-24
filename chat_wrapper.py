
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from termcolor import colored
from langgraph.graph import END, StateGraph, START
from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_together import ChatTogether
from utils.checkpointer import checkpointer
import json
load_dotenv()
model = ChatTogether(
    api_key = os.getenv("TOGETHER_API_KEY"),
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

class ChatState(MessagesState):
    should_end: bool
    hotel_determined: str
    intent: str
def call_model(state: ChatState):
    # Getting data from RAG and KB to added here (Hardcoding values for now) 
    kb_mock_data = """
<resorts>
    <resort>
        <id>1</id>
        <name>Sterling Rudraksh Jaisalmer</name>
        <zone>West</zone>
        <state>Rajasthan</state>
        <city>Jaisalmer</city>
    </resort>
    <resort>
        <id>2</id>
        <name>Sterling Bagh Ranthambore</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Ranthambore</city>
    </resort>
    <resort>
        <id>3</id>
        <name>Sterling Lontano Waterfront Wayanad</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Wayanad</city>
    </resort>
    <resort>
        <id>4</id>
        <name>Sterling Oriental Woods, Pench</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Ramtek, Pench</city>
    </resort>
    <resort>
        <id>5</id>
        <name>Sterling City Centre Bokaro</name>
        <zone>East</zone>
        <state>Jharkhand</state>
        <city>Bokaro</city>
    </resort>
    <resort>
        <id>6</id>
        <name>HSD TEAM DETAILS</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Chennai</city>
    </resort>
    <resort>
        <id>7</id>
        <name>Sterling Aravali, Udaipur</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Udaipur</city>
    </resort>
    <resort>
        <id>8</id>
        <name>Sterling Marbella, Dehradun</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Dehradun</city>
    </resort>
    <resort>
        <id>9</id>
        <name>Sterling Stolen Heaven Lonavala</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Lonavala</city>
    </resort>
    <resort>
        <id>10</id>
        <name>Sterling Banashree Badami</name>
        <zone>South</zone>
        <state>Karnataka</state>
        <city>Badami</city>
    </resort>
    <resort>
        <id>11</id>
        <name>STERLING CORE VALUES</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Chennai</city>
    </resort>
    <resort>
        <id>12</id>
        <name>STERLING CIRCLE</name>
        <zone>North</zone>
        <state>Delhi</state>
        <city>Delhi</city>
    </resort>
    <resort>
        <id>13</id>
        <name>Sterling Pushkar</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Pushkar</city>
    </resort>
    <resort>
        <id>14</id>
        <name>BRAND ASSOCIATIONS</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Chennai</city>
    </resort>
    <resort>
        <id>15</id>
        <name>Sterling Athirappilly</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Athirappilly</city>
    </resort>
    <resort>
        <id>16</id>
        <name>Sterling Jaisinghgarh Udaipur</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Udaipur</city>
    </resort>
    <resort>
        <id>17</id>
        <name>Sterling Balicha Udaipur</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Udaipur</city>
    </resort>
    <resort>
        <id>18</id>
        <name>Sterling Vythiri, Wayanad</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Wayanad</city>
    </resort>
    <resort>
        <id>19</id>
        <name>PHOTOS VIDEOS CLIENT FEED BACKS (ALL RESORTS)</name>
        <zone>North</zone>
        <state>Delhi</state>
        <city>Delhi</city>
    </resort>
    <resort>
        <id>20</id>
        <name>Sterling Panchgani</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Panchgani</city>
    </resort>
    <resort>
        <id>21</id>
        <name>Sterling Legacy Shimla</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Shimla</city>
    </resort>
    <resort>
        <id>22</id>
        <name>Sterling Nature Trails Kundalika, Kolad</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Kolad</city>
    </resort>
    <resort>
        <id>23</id>
        <name>Sterling Nature Trails Sajan, Vikramgad</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>VIikramgad</city>
    </resort>
    <resort>
        <id>24</id>
        <name>Sterling Nature Trails Durshet, Khopoli</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Khapoli</city>
    </resort>
    <resort>
        <id>25</id>
        <name>Sterling Kodai Valley</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Kodaikanal</city>
    </resort>
    <resort>
        <id>26</id>
        <name>Sterling Kodai Lake</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Kodaikanal</city>
    </resort>
    <resort>
        <id>27</id>
        <name>Sterling Ooty- Fern Hill</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Ooty</city>
    </resort>
    <resort>
        <id>28</id>
        <name>Sterling Ooty- Elk Hill</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Ooty</city>
    </resort>
    <resort>
        <id>29</id>
        <name>Sterling Yercaud</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Yercaud</city>
    </resort>
      <resort>
        <id>30</id>
        <name>Sterling Yelagiri</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Yelagiri</city>
    </resort>
    <resort>
        <id>31</id>
        <name>Sterling Arunai Anantha Tiruvammamalai</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Tiruvannamalai</city>
    </resort>
    <resort>
        <id>32</id>
        <name>Sterling V Grand Madurai</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Madurai</city>
    </resort>
    <resort>
        <id>33</id>
        <name>Sterling Wayanad</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Wayanad</city>
    </resort>
    <resort>
        <id>34</id>
        <name>Sterling Munnar</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Munnar</city>
    </resort>
    <resort>
        <id>35</id>
        <name>Sterling Lake Palace Alleppey</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Alleppey</city>
    </resort>
    <resort>
        <id>36</id>
        <name>Sterling Guruvayur</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Guruvayur</city>
        <status>Active</status>  <resort>
        <id>30</id>
        <name>Sterling Yelagiri</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Yelagiri</city>
    </resort>
    <resort>
        <id>31</id>
        <name>Sterling Arunai Anantha Tiruvammamalai</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Tiruvannamalai</city>
    </resort>
    <resort>
        <id>32</id>
        <name>Sterling V Grand Madurai</name>
        <zone>South</zone>
        <state>Tamil Nadu</state>
        <city>Madurai</city>
    </resort>
    <resort>
        <id>33</id>
        <name>Sterling Wayanad</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Wayanad</city>
    </resort>
    <resort>
        <id>34</id>
        <name>Sterling Munnar</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Munnar</city>
    </resort>
    <resort>
        <id>35</id>
        <name>Sterling Lake Palace Alleppey</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Alleppey</city>
    </resort>
    <resort>
        <id>36</id>
        <name>Sterling Guruvayur</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Guruvayur</city>
    </resort>
    <resort>
        <id>37</id>
        <name>Sterling Anaikatti</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Anaikatti</city>
    </resort>
    <resort>
        <id>38</id>
        <name>Sterling Thekkady</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Thekkady</city>
    </resort>
    <resort>
        <id>39</id>
        <name>Sterling Palavelli Godavari</name>
        <zone>South</zone>
        <state>Andhra Pradesh</state>
        <city>Yalamanchalli Lanka</city>
    </resort>
    <resort>
        <id>40</id>
        <name>Sterling Puri</name>
        <zone>East</zone>
        <state>Odisha</state>
        <city>Puri</city>
    </resort>
    <resort>
        <id>41</id>
        <name>Sterling Gangtok Orange Village</name>
        <zone>East</zone>
        <state>Sikkim</state>
        <city>Gangtok</city>
    </resort>
    <resort>
        <id>42</id>
        <name>Sterling Park Kalimpong</name>
        <zone>East</zone>
        <state>West Bengal</state>
        <city>Kalimpong</city>
    </resort>
    <resort>
        <id>43</id>
        <name>Sterling Darjeeling</name>
        <zone>East</zone>
        <state>West Bengal</state>
        <city>Darjeeling</city>
    </resort>
    <resort>
        <id>44</id>
        <name>Sterling Karwar</name>
        <zone>West</zone>
        <state>Karnataka</state>
        <city>Karwar</city>
    </resort>
    <resort>
        <id>45</id>
        <name>Sterling Gir</name>
        <zone>West</zone>
        <state>Gujarat</state>
        <city>Sasan Gir</city>
    </resort>
    <resort>
        <id>46</id>
        <name>Sterling Lonavala</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Lonavala</city>
    </resort>
    <resort>
        <id>47</id>
        <name>Sterling Goa Varca</name>
        <zone>West</zone>
        <state>Goa</state>
        <city>Goa-Varca</city>
    </resort>
    <resort>
        <id>48</id>
        <name>Sterling Padam Pench</name>
        <zone>North</zone>
        <state>Madhya Pradesh</state>
        <city>Pench</city>
    </resort>
    <resort>
        <id>49</id>
        <name>Sterling Kanha</name>
        <zone>North</zone>
        <state>Madhya Pradesh</state>
        <city>Kanha</city>
    </resort>
    <resort>
        <id>50</id>
        <name>Sterling Mount Abu</name>
        <zone>West</zone>
        <state>Rajasthan</state>
        <city>Mount Abu</city>
    </resort>
    <resort>
        <id>51</id>
        <name>Sterling Rewild Sariska</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Sariska</city>
    </resort>
    <resort>
        <id>52</id>
        <name>Sterling Manali</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Manali</city>
    </resort>
    <resort>
        <id>53</id>
        <name>Sterling Shivalik Chail</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Chail</city>
    </resort>
    <resort>
        <id>54</id>
        <name>Sterling Kufri</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Kufri</city>
    </resort>
    <resort>
        <id>55</id>
        <name>Sterling Corbett</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Corbett</city>
    </resort>
    <resort>
        <id>56</id>
        <name>Sterling Nainital</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Nainital</city>
    </resort>
    <resort>
        <id>57</id>
        <name>Sterling Mantra Haridwar</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Haridwar</city>
    </resort>
    <resort>
        <id>58</id>
        <name>Sterling Palm Bliss Rishikesh</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Rishikesh</city>
    </resort>
    <resort>
        <id>59</id>
        <name>Sterling Mussoorie</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Mussoorie</city>
    </resort>
    <resort>
        <id>60</id>
        <name>De Laila Houseboats-Srinagar</name>
        <zone>North</zone>
        <state>Jammu and Kashmir</state>
        <city>Srinagar</city>
        <
    </resort>
    <resort>
        <id>37</id>
        <name>Sterling Anaikatti</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Anaikatti</city>
    </resort>
    <resort>
        <id>38</id>
        <name>Sterling Thekkady</name>
        <zone>South</zone>
        <state>Kerala</state>
        <city>Thekkady</city>
    </resort>
    <resort>
        <id>39</id>
        <name>Sterling Palavelli Godavari</name>
        <zone>South</zone>
        <state>Andhra Pradesh</state>
        <city>Yalamanchalli Lanka</city>
    </resort>
    <resort>
        <id>40</id>
        <name>Sterling Puri</name>
        <zone>East</zone>
        <state>Odisha</state>
        <city>Puri</city>
    </resort>
    <resort>
        <id>41</id>
        <name>Sterling Gangtok Orange Village</name>
        <zone>East</zone>
        <state>Sikkim</state>
        <city>Gangtok</city>
    </resort>
    <resort>
        <id>42</id>
        <name>Sterling Park Kalimpong</name>
        <zone>East</zone>
        <state>West Bengal</state>
        <city>Kalimpong</city>
    </resort>
    <resort>
        <id>43</id>
        <name>Sterling Darjeeling</name>
        <zone>East</zone>
        <state>West Bengal</state>
        <city>Darjeeling</city>
    </resort>
    <resort>
        <id>44</id>
        <name>Sterling Karwar</name>
        <zone>West</zone>
        <state>Karnataka</state>
        <city>Karwar</city>
    </resort>
    <resort>
        <id>45</id>
        <name>Sterling Gir</name>
        <zone>West</zone>
        <state>Gujarat</state>
        <city>Sasan Gir</city>
    </resort>
    <resort>
        <id>46</id>
        <name>Sterling Lonavala</name>
        <zone>West</zone>
        <state>Maharashtra</state>
        <city>Lonavala</city>
    </resort>
    <resort>
        <id>47</id>
        <name>Sterling Goa Varca</name>
        <zone>West</zone>
        <state>Goa</state>
        <city>Goa-Varca</city>
    </resort>
    <resort>
        <id>48</id>
        <name>Sterling Padam Pench</name>
        <zone>North</zone>
        <state>Madhya Pradesh</state>
        <city>Pench</city>
    </resort>
    <resort>
        <id>49</id>
        <name>Sterling Kanha</name>
        <zone>North</zone>
        <state>Madhya Pradesh</state>
        <city>Kanha</city>
    </resort>
    <resort>
        <id>50</id>
        <name>Sterling Mount Abu</name>
        <zone>West</zone>
        <state>Rajasthan</state>
        <city>Mount Abu</city>
    </resort>
    <resort>
        <id>51</id>
        <name>Sterling Rewild Sariska</name>
        <zone>North</zone>
        <state>Rajasthan</state>
        <city>Sariska</city>
    </resort>
    <resort>
        <id>52</id>
        <name>Sterling Manali</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Manali</city>
    </resort>
    <resort>
        <id>53</id>
        <name>Sterling Shivalik Chail</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Chail</city>
    </resort>
    <resort>
        <id>54</id>
        <name>Sterling Kufri</name>
        <zone>North</zone>
        <state>Himachal Pradesh</state>
        <city>Kufri</city>
    </resort>
    <resort>
        <id>55</id>
        <name>Sterling Corbett</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Corbett</city>
    </resort>
    <resort>
        <id>56</id>
        <name>Sterling Nainital</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Nainital</city>
    </resort>
    <resort>
        <id>57</id>
        <name>Sterling Mantra Haridwar</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Haridwar</city>
    </resort>
    <resort>
        <id>58</id>
        <name>Sterling Palm Bliss Rishikesh</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Rishikesh</city>
    </resort>
    <resort>
        <id>59</id>
        <name>Sterling Mussoorie</name>
        <zone>North</zone>
        <state>Uttarakhand</state>
        <city>Mussoorie</city>
    </resort>
    <resort>
        <id>60</id>
        <name>De Laila Houseboats-Srinagar</name>
        <zone>North</zone>
        <state>Jammu and Kashmir</state>
        <city>Srinagar</city>
    </resort>
</resorts>
    
    
    """
    prompt = """ 
            You work for Sterling hotels and you are the chain manager agent. Your primary focus is to guide the user to select a hotel as per their requirements and our hotel availability at the given locations.
            
            The users can either be in any one of these two categories:
                1. One who knows exactly about the hotel property that they want to interact with.
                2. One who is trying to find the best hotel for them based on their preferences.You are the manager agent who guides the user to select a hotel at a location as per their requirements and Sterling's hotel locations.
            

            Your only task is to determine the best hotel for the user based on their preferences.
            If you have the hotel determined and then the user asks you to book,cancel,modify,check availability about rooms or any other enquiry about rooms then return the JSON output mentioned below without waiting for "CONFIRM":
            You primary focus is to guide the user to select a hotel as per their requirements and our hotel availability at the given locations.
            
            When you believe you figured out the user's preferred hotel:
            - Return the JSON output mentioned below:

            Output Format Rules:
            - When sending the final task, only output this JSON object.
            - Format must be exactly:
                {{
                "should_end": "True",
                "hotel_determined": hotel_name_finalised(null if not determined),
                "intent": intent
                }}
            - No other text should be included before or after the JSON.
            - The task_determined should clearly specify which tool and method was chosen
            Error Handling:
            - If users request something outside the available options, politely explain what is possible
            - If users seem confused, break down the options into simpler choices
            - If users change their mind, be flexible and help them find the right alternative
            - If users don't type "CONFIRM", continue the conversation without outputting the JSON

            Remember:
            - It should feel very conversational to the user.
            - Do not ask for all the inputs at once.
            - You have to be conversational like a support staff.
            - You don't have to beat around the bush a lot be direct but polite and keep hospitality in mind.
            - Give one short liners as response and act like a human persona with a fictional name.
            - Only output the JSON after receiving "CONFIRM"
            - Never include any other text with the JSON output
            - You cannot mention what role you have in Sterling Hotels.
            - If the user asks about hotel amenties then don't assume details if not provided to you.
            - If the user asks you to book,cancel,modify,check availability about rooms or any other task then return the JSON output mentioned without waiting for "CONFIRM"

            Details about Sterling Chain of Hotels:
            <locations>{kb_mock_data}</locations>
            
            \n
            """.format(kb_mock_data=kb_mock_data)

    system_prompt = (
        prompt)
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    state["messages"].append(response)
    # print(colored(state['state_variables'],"yellow"))
    return state

workflow = StateGraph(state_schema=ChatState)

workflow.add_node("model", call_model)
workflow.add_edge(START, "model")
workflow.add_edge("model",END)

# Add simple in-memory checkpointer
# memory = MemorySaver()

# TEMP
app = workflow.compile(checkpointer=checkpointer)

def stream_graph_updates(state):
    init_state = ChatState(
        messages=state['messages']
    )
    config = {"configurable": {"thread_id": state['thread_id']}}
    for state in app.stream(init_state,config):
            ai_response = state['model']['messages'][-1].content
            print(colored(ai_response,"green"))
            ai_response= ai_response.replace('```json\n', '').replace('\n```', '')
            try:
                response_data = json.loads(ai_response)
                if "should_end" in response_data and response_data['should_end']:
                    obj = response_data
            except json.JSONDecodeError:
                obj = {"inner_messages":state['model']['messages']}
                pass
            return obj



# while True:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         response_data = stream_graph_updates(user_input)
#         if "should_end" in response_data and response_data['should_end']:
#             break
#
    
            # ai_response= ai_response.replace('```json\n', '').replace('\n```', '')
            # try:
            #     response_data = json.loads(ai_response)
            #     if "should_end" in response_data and response_data['should_end']:
            #         final_task.append(response_data.get('task_determined'))
            #         print(colored(final_task[-1],"yellow"))
            #         obj = {"task_ready":True,"task":final_task[-1]}
            #     elif "should_execute" in response_data and response_data['should_execute']:
            #         obj = {"should_execute":True}
            # except json.JSONDecodeError:
            #     obj = {"inner_messages":state['model']['messages']}
            #     pass
#

def chat_subgraph_wrapper(state):
    app = workflow.compile(checkpointer=memory)
    init_state = ChatState(
        messages=state['messages'],
        state_variables=str(list(state.keys())),
        has_optimal_path = state['has_optimal_path']
    )
    config = {"configurable": {"thread_id": state['thread_id']}}
    for state in app.stream(init_state,config):
            ai_response = state['model']['messages'][-1].content
            # print(colored(state['model']['messages'],"red"))
            ai_response= ai_response.replace('```json\n', '').replace('\n```', '')

            try:
                response_data = json.loads(ai_response)
                if "should_end" in response_data and response_data['should_end']:
                    final_task.append(response_data.get('task_determined'))
                    print(colored(final_task[-1],"yellow"))
                    obj = {"task_ready":True,"task":final_task[-1]}
                elif "should_execute" in response_data and response_data['should_execute']:
                    obj = {"should_execute":True}
            except json.JSONDecodeError:
                obj = {"inner_messages":state['model']['messages']}
                pass
            return obj
            
            

        
