from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import nltk
import sys
import turtle
import math
import os.path
import random
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from autocorrect import spell
import ttkSimpleDialog as tkSimpleDialog

class ResearchTool:
    def __init__(self, master):
        self.var1 = IntVar(value = 1)
        self.var2 = IntVar(value = 1)
        self.var2A = IntVar(value = 0)
        self.var3 = IntVar(value = 1)
        self.var4 = IntVar(value = 1)
        self.var4A = IntVar(value = 0)
        self.var5 = IntVar(value = 1)
        self.master = master
        self.frame = Frame(root, bd=2, relief="sunken")
        self.entry_1 = Entry(root, width=70)
        self.entry_1.config(font=("Courier New", 10))
        self.label_0 = Label(root, text="Conceptual Model Tool v3.0")
        self.label_0.config(font=("Courier New", 20,'bold'))
        self.label_1 = Label(root, text="User Stories:")
        self.label_1.config(font=("Courier New", 10))
        self.checkbutton_1 = Checkbutton(root,text = "Canonical Form",variable = self.var1)
        self.checkbutton_1.config(font=("Courier New", 10))
        self.checkbutton_2 = Checkbutton(root,text = "Domain Model - All",variable = self.var2)
        self.checkbutton_2.config(font=("Courier New", 10))
        self.checkbutton_2A = Checkbutton(root,text = "Domain Model(s) - Agent Level",variable = self.var2A)
        self.checkbutton_2A.config(font=("Courier New", 10))
        self.checkbutton_3 = Checkbutton(root,text = "Process Model",variable = self.var3)
        self.checkbutton_3.config(font=("Courier New", 10))
        self.checkbutton_4 = Checkbutton(root,text = "State Machine(s) - Object Level",variable = self.var4)
        self.checkbutton_4.config(font=("Courier New", 10))
        self.checkbutton_4A = Checkbutton(root,text = "Include 2- & 3-step Transitions in the State Machine(s)",variable = self.var4A)
        self.checkbutton_4A.config(font=("Courier New", 8))
        self.checkbutton_5 = Checkbutton(root,text = "Use Case - UML Format",variable = self.var5)
        self.checkbutton_5.config(font=("Courier New", 10))
        self.text_0 = Text(root, height = 16,width = 70)
        self.scroll = Scrollbar(root, command=self.text_0.yview)
        self.text_0.config(font=("Courier New", 10), yscrollcommand=self.scroll.set)
        self.label_2 = Label(root, text="Messages:")
        self.label_2.config(font=("Courier New", 10))
       
    def create_screen(self):
        self.label_0.grid(row=1, column=1, padx = 20,pady = 20)
        self.button_browse = Button(root, text="Browse", width=10, height=1, command=self.access_file)
        self.button_browse.config(font=("Courier New", 10))
        self.button_generate = Button(root, text="Generate", width=10, height=1, command=self.generate_model)
        self.button_generate.config(font=("Courier New", 10),state=DISABLED)
        self.label_1.grid(row=2,column=0,padx = 20,pady = 20)
        self.entry_1.grid(row=2,column=1,padx = 0,pady = 0)
        self.button_browse.grid(row=2,column=2,padx = 20,pady = 20)

        self.checkbutton_1.grid(row=3,column = 1,sticky = W,padx = 80)
        self.checkbutton_2.grid(row=4,column = 1,sticky = W,padx = 80)
        self.checkbutton_2A.grid(row=5,column = 1,sticky = W,padx = 80)
        self.checkbutton_3.grid(row=6,column = 1,sticky = W,padx = 80)
        self.checkbutton_4.grid(row=7,column = 1,sticky = W,padx = 80)
        self.checkbutton_4A.grid(row=8,column = 1,sticky = W,padx = 80)
        self.checkbutton_5.grid(row=9,column = 1,sticky = W,padx = 80)

        self.button_generate.grid(row=10, column=1,padx = 10,pady = 10)
        self.label_2.grid(row=11, column=0, padx=20, pady=20)
        self.text_0.grid(row=11,column=1,padx = 20,pady = 20)
        self.scroll.grid(row=11, column=1, sticky=N + S + E)

    def access_file(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.button_generate.config(state=NORMAL)
        temparray = []
        temparray = root.filename.split("/")
        root.filelocation = ""
        for i in range(0,len(temparray)-1):
            if root.filelocation == "":
                root.filelocation = temparray[i]
            else:
                root.filelocation = root.filelocation + "\\" + temparray[i]

        self.entry_1.delete(0, "end")
        self.entry_1.insert(0,root.filename)

    def extractComponents(self):

        files = []
        Lem = WordNetLemmatizer()

        self.button_generate.config(state=DISABLED)
        test = os.listdir(root.filelocation)

        for item in test:
            if (item.startswith("ERD") or item.startswith("BPMN") or item.startswith("FSM") or item.startswith("USE")) and item.endswith(".eps"):
                os.remove(root.filelocation + "\\" + item)
            if item.endswith(".xml"):
                os.remove(root.filelocation + "\\" + item)
            if item.startswith("CANONICAL") and item.endswith(".csv"):
                try:
                    os.remove(root.filelocation + "\\" + item)
                except:
                    self.text_0.insert(END, "\n" + "ERROR: Output file CANONICAL FORM.csv is open!\n")
                    self.text_0.see(END)
                    return


        from nltk.corpus import sentiwordnet as swn
        from nltk.tag.perceptron import PerceptronTagger
        from nltk.tokenize import word_tokenize

        self.text_0.insert(END,"Working on it...\n")
        self.text_0.see(END)

        myfile = open(root.filename)
        mytxt1 = myfile.read()
        mytxt1 = mytxt1.lower()
        mytxt1 = mytxt1.split("\n")

        storycount = 0

        agent = []
        action = []
        object = []
        preconcept = []
        precondition = []
        postconcept = []
        postcondition = []
        andposition = []
        andposition2 = []
        preconcepttype = []
        postconcepttype = []

        for mytxt in mytxt1:

            andposition = []

            andposition2 = []

            andindicator = ""

            andindicator2 = ""

            passiveindicator = False

            if mytxt != "" and mytxt[:1] != "#":

                if " as " not in mytxt.lower() or " i " not in mytxt.lower() or " so " not in mytxt.lower() or " given " not in mytxt.lower() or " when " not in mytxt.lower() or " then " not in mytxt.lower():
                    self.text_0.insert(END, "\n" + "ERROR: Following user story is not in the desired format:\n" + mytxt + "\n")
                    self.text_0.see(END)
                    return

                first = -1
                second = -1
                third = -1
                fourth = -1
                fifth = -1
                sixth = -1

                tokens = nltk.word_tokenize(mytxt)
                tagged = nltk.pos_tag(tokens)
                entities = nltk.chunk.ne_chunk(tagged)

                for i in range(0, len(entities) - 1):
                    if entities[i][0] == "as" and first < 0:
                        first = i
                    if entities[i][0] == "i" and first > 0 and second < 0:
                        second = i
                    if entities[i][0] == "so" and second > 0 and third < 0:
                        third = i
                    if entities[i][0] == "given" and third > 0 and fourth < 0:
                        fourth = i
                        andposition.append(i)
                    if (entities[i][0] == "and" or entities[i][0] == "or") and fourth > 0 and fifth < 0:
                        andposition.append(i)
                        if entities[i][0] == "and":
                            andindicator = "[+]"
                        elif entities[i][0] == "or":
                            if messagebox.askquestion ("Question","Does the percondition of the following user story contain an exclusive or?\n\n" + mytxt,icon = "question") == "yes":
                                andindicator = "[x]"
                            else:
                                andindicator = "[o]"
                    if entities[i][0] == "when" and fourth > 0 and fifth < 0:
                        fifth = i
                        andposition.append(i)
                    if entities[i][0] == "then" and fifth > 0 and sixth < 0:
                        sixth = i
                        andposition2.append(i)
                    if (entities[i][0] == "and") and sixth > 0:
                        andposition2.append(i)
                        andindicator2 = "[+]"

                andposition2.append(len(entities) - 1)

                agentpresent = False
                objectpresent = False
                preconceptpresent = False
                preconceptindex = -1
                postconceptpresent = False
                postconceptindex = -1

                for i in range(0, len(entities) - 1):
                    if i > first and i < second:
                        if (entities[i][1] == "NN" or entities[i][1] == "NNS" or entities[i][1] == "RB" or entities[i][1] == "JJ"):
                            if agentpresent == False:
                                try:
                                    agent.append(entities[i][0])
                                except:
                                    agent.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","Who is the actor of the following user story?\n\n" + mytxt).lower()))
                                agentbackup = entities[i][0]
                                agentpresent = True
                            else:
                                agent[len(agent) - 1] = agent[len(agent) - 1] + " " + entities[i][0]
                                agentbackup = agent[len(agent) - 1]
                    if i > second and i < third:
                        if passiveindicator == False:
                            if (entities[i][1] == "NN" or entities[i][1] == "NNS" or entities[i][1] == "RB" or entities[i][1] == "JJ"):
                                if objectpresent == False:
                                    try:
                                        object.append(entities[i][0])
                                    except:
                                        object.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What object is acted on in the following user story?\n\n" + mytxt).lower()))
                                    objectbackup = entities[i][0]
                                    objectpresent = True
                                else:
                                    object[len(object) - 1] = object[len(object) - 1] + " " + entities[i][0]
                                    objectbackup = object[len(object) - 1]
                            if entities[i][1] == "VB":
                                try:
                                    action.append(entities[i][0])
                                except:
                                    action.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What is the action of the actor in the following user story?\n\n" + mytxt).lower()))
                                actionindexbackup = i
                            if entities[i][1] == "IN":
                                if i - 1 == actionindexbackup:
                                    action[len(action) - 1] = action[len(action) - 1] + " " + entities[i][0]

                            if entities[i][1] == "VBN" and entities[i-1][0] == "be":
                                object.append(agent[len(agent) - 1])
                                agent[len(agent) - 1] = "system"
                                action[len(action) - 1] = WordNetLemmatizer().lemmatize(entities[i][0], 'v')
                                passiveindicator = True
                                longaction = ""
                                for kk in range(0, len(entities) - 1):
                                    if kk > i + 1 and kk < third:
                                        if longaction == "":
                                            longaction = " " + entities[kk][0]
                                        else:
                                            longaction = longaction + " " + entities[kk][0] 
                                action[len(action) - 1] = action[len(action) - 1] + longaction + " to"

                    for k in range(0, len(andposition) - 1):
                        if i > andposition[k] and i < andposition[k + 1]:
                            if (entities[i][1] == "NN" or entities[i][1] == "NNS" or entities[i][1] == "RB"):
                                if preconceptpresent == False or preconceptindex != i - 1:
                                    try:
                                        preconcept.append(entities[i][0])
                                        preconcepttype.append(andindicator)
                                    except:
                                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in precondition:\n" + mytxt + "\n")
                                        self.text_0.see(END)
                                        return
                                    preconceptbackup = entities[i][0]
                                    preconceptpresent = True
                                    preconceptindex = i
                                else:
                                    preconcept[len(preconcept) - 1] = preconcept[len(preconcept) - 1] + " " + entities[i][0]
                                    preconceptbackup = preconcept[len(preconcept) - 1]
                            if (entities[i][1] == "JJ" or entities[i][1] == "VBN"):
                                try:
                                    precondition.append(entities[i][0])
                                except:
                                    self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a precondition:\n" + mytxt + "\n")
                                    self.text_0.see(END)
                                    return
                    for k in range(0, len(andposition2) - 1):
                        if i > andposition2[k] and i < andposition2[k + 1]:
                            if (entities[i][1] == "NN" or entities[i][1] == "NNS" or entities[i][1] == "RB"):
                                if postconceptpresent == False or postconceptindex != i - 1:
                                    try:
                                        postconcept.append(entities[i][0])
                                        postconcepttype.append(andindicator2)
                                    except:
                                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in postcondition:\n" + mytxt + "\n")
                                        self.text_0.see(END)
                                        return
                                    postconceptbackup = entities[i][0]
                                    postconceptpresent = True
                                    postconceptindex = i
                                else:
                                    postconcept[len(postconcept) - 1] = postconcept[len(postconcept) - 1] + " " + entities[i][0]
                                    postconceptbackup = postconcept[len(postconcept) - 1]
                            if (entities[i][1] == "JJ" or entities[i][1] == "VBN"):
                                try:
                                    postcondition.append(entities[i][0])
                                except:
                                    self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a postcondition:\n" + mytxt + "\n")
                                    self.text_0.see(END)
                                    return

                if len(object) < len(agent):
                    try:
                        object.append(object[len(object) - 1])
                    except:
                        object.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What object is acted on in the following user story?\n\n" + mytxt).lower()))
                if len(preconcept) < len(object):
                    if len(preconcept) < len(agent):
                        try:
                            preconcept.append(object[len(object) - 1])
                            preconcepttype.append(andindicator)
                        except:
                            self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in precondition:\n" + mytxt + "\n")
                            self.text_0.see(END)
                            return
                    else:
                        try:
                            preconcept.append(preconcept[len(preconcept) - 1])
                            preconcepttype.append(andindicator)
                        except:
                            self.text_0.insert(END, "\n" + "ERROR: Following user story has a problem with an agent/object in precondition:\n" + mytxt + "\n")
                            self.text_0.see(END)
                            return

                if len(postconcept) < len(preconcept):
                    if len(postconcept) < len(agent):
                        try:
                            postconcept.append(preconcept[len(preconcept) - 1])
                            postconcepttype.append(andindicator2)
                        except:
                            self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in postcondition:\n" + mytxt + "\n")
                            self.text_0.see(END)
                            return
                    else:
                        try:
                            postconcept.append(postconcept[len(postconcept) - 1])
                            postconcepttype.append(andindicator2)
                        except:
                            self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in postcondition:\n" + mytxt + "\n")
                            self.text_0.see(END)
                            return

                if len(precondition) > len(agent) or len(postcondition) > len(agent):
                    try:
                        agent.append(agent[len(agent) - 1])
                    except:
                        agent.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","Who is the actor of the following user story?\n\n" + mytxt).lower()))
                if len(precondition) > len(action) or len(postcondition) > len(action):
                    try:
                        action.append(action[len(action) - 1])
                    except:
                        action.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What is the action of the actor in the following user story?\n\n" + mytxt).lower()))
                if len(precondition) > len(object) or len(postcondition) > len(object):
                    try:
                        object.append(object[len(object) - 1])
                    except:
                        object.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What object is acted on in the following user story?\n\n" + mytxt).lower()))
                if len(precondition) > len(preconcept) or len(postcondition) > len(preconcept):
                    try:
                        preconcept.append(preconcept[len(preconcept) - 1])
                        preconcepttype.append(andindicator)
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in precondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(precondition) > len(postconcept) or len(postcondition) > len(postconcept):
                    try:
                        postconcept.append(postconcept[len(postconcept) - 1])
                        postconcepttype.append(andindicator2)
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in postcondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(precondition) > len(postcondition):
                    try:
                        postcondition.append(postcondition[len(postcondition) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a postcondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(postcondition) > len(precondition):
                    try:
                        precondition.append(precondition[len(precondition) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a precondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(preconcept) > len(agent) or len(postconcept) > len(agent):
                    try:
                        agent.append(agent[len(agent) - 1])
                    except:
                        agent.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","Who is the actor of the following user story?\n\n" + mytxt).lower()))
                if len(preconcept) > len(action) or len(postconcept) > len(action):
                    try:
                        action.append(action[len(action) - 1])
                    except:
                        action.append(Lem.lemmatize(tkSimpleDialog.askstring("Question","What is the action of the actor in the following user story?\n\n" + mytxt).lower()))
                if len(preconcept) > len(object) or len(postconcept) > len(object):
                    try:
                        object.append(object[len(object) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with object:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(preconcept) > len(precondition) or len(postconcept) > len(precondition):
                    try:
                        precondition.append(precondition[len(precondition) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a precondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(preconcept) > len(postconcept):
                    try:
                        postconcept.append(postconcept[len(postconcept) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in postcondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(postconcept) > len(preconcept):
                    try:
                        preconcept.append(preconcept[len(preconcept) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with an agent/object in precondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return
                if len(preconcept) > len(postcondition) or len(postconcept) > len(postcondition):
                    try:
                        postcondition.append(postcondition[len(postcondition) - 1])
                    except:
                        self.text_0.insert(END,"\n" + "ERROR: Following user story has a problem with a postcondition:\n" + mytxt + "\n")
                        self.text_0.see(END)
                        return

                storycount = storycount + 1

        if self.validateTable(agent, action, object, preconcept, precondition, postconcept, postcondition) == False:
            exit()

        for i in range (0, len(agent)):
            presentInd = False
            for j in range (0,i):
                if preconcept[i] == postconcept[j] and precondition[i] == postcondition[j]:
                    presentInd = True
            if presentInd == False:
                preconcepttype[i] = ""

        for i in range(1, len(agent)):
            if agent[i] == agent[i-1] and action[i] == action[i-1] and object[i] == object[i-1]:
                if preconcepttype [i] == "" or preconcepttype [i-1] == "":
                    preconcepttype[i] = ""
                    preconcepttype[i-1] = ""

        #self.preconditionsymbol(action, preconcept, precondition, postconcept, postcondition, preconcepttype)
        self.postconditionsymbol(preconcept, precondition, postconcept, postcondition, postconcepttype)

        self.text_0.insert(END,"\n" + str(storycount) + " user stories identified..." + "\n")
        self.text_0.see(END)

        if self.var1.get() == 1:
            try:
                f = open(root.filelocation + "\\CANONICAL FORM.csv", 'w+')
            except:
                self.text_0.insert(END, "\n" + "ERROR: Output file CANONICAL FORM.csv is open!\n")
                self.text_0.see(END)
                return

            f.write("agent,action,object,agent/object,precondition,agent/object,postcondition,gateway-in,gateway-out" + "\n")
            for i in range(0, len(agent)):
                agent[i] = Lem.lemmatize(agent[i])
                action[i] = Lem.lemmatize(action[i])
                object[i] = Lem.lemmatize(object[i])
                preconcept[i] = Lem.lemmatize(preconcept[i])
                precondition[i] = Lem.lemmatize(precondition[i])
                postconcept[i] = Lem.lemmatize(postconcept[i])
                postcondition[i] = Lem.lemmatize(postcondition[i])
                f.write(agent[i] + "," + action[i] + "," + object[i] + "," + preconcept[i] + "," + precondition[
                    i] + "," + postconcept[i] + "," + postcondition[i] + "," + preconcepttype[i] + "," + postconcepttype[i] + "\n")
            f.close()

        turtle.setup(width = 1.0, height = 1.0)
        turtle.Screen()

        if self.var2.get() == 1:
            self.drawER(agent, action, object, files, "all")
            self.drawDomainXML(agent, action, object, files)

        if self.var2A.get() == 1:
            conceptU = []

            for i in range(0, len(agent)):
                present = False
                for j in range(0, len(conceptU)):
                    if agent[i] == conceptU[j]:
                        present = True
                if present == False:
                    conceptU.append(agent[i])

            for i in range(0, len(conceptU)):
                agentU = []
                actionU = []
                objectU = []
                for j in range(0,len(agent)):
                    if conceptU[i] == agent[j]:
                        agentU.append(agent[j])
                        actionU.append(action[j])
                        objectU.append(object[j])

                self.drawER(agentU, actionU, objectU, files, conceptU[i])

        if self.var3.get() == 1:
            self.drawBPMN(agent, action, object, preconcept, precondition, postconcept, postcondition, preconcepttype, postconcepttype, files)
            self.drawProcessModelXML(agent, action, object, preconcept, precondition, postconcept, postcondition, preconcepttype, postconcepttype, files)

        if self.var4.get() == 1:
            condition1 = []
            condition2 = []

            for i in range(0, len(preconcept)):
                condition1.append(preconcept[i])

            for i in range(0, len(postconcept)):
                condition1.append(postconcept[i])

            for i in range(0, len(precondition)):
                condition2.append(precondition[i])

            for i in range(0, len(postcondition)):
                condition2.append(postcondition[i])

            condition = []
            for i in range(0, len(preconcept)):
                present = False
                present1 = False
                for j in range(0, len(condition)):
                    if preconcept[i] == condition[j]:
                        present = True
                for k in range(0, len(object)):
                    if preconcept[i] == object[k]:
                        present1 = True
                if present == False and present1 == True:
                    condition.append(preconcept[i])

            for i in range(0, len(postconcept)):
                present = False
                present1 = False
                for j in range(0, len(condition)):
                    if postconcept[i] == condition[j]:
                        present = True
                for k in range(0, len(object)):
                    if postconcept[i] == object[k]:
                        present1 = True
                if present == False and present1 == True:
                    condition.append(postconcept[i])

            for i in range(0, len(condition)):
                state = []
                for j in range(0, len(condition1)):
                    if condition[i] == condition1[j]:
                        state.append(condition2[j])

                state1 = []
                state1.append("unknown")
                orphanstate1 = []
                orphanstate1.append("*")
                childlessstate1 = []
                childlessstate1.append("*")
                for k in range(0, len(state)):
                    present = False
                    for j in range(0, len(state1)):
                        if state[k] == state1[j]:
                            present = True
                    if present == False:
                        state1.append(state[k])
                        orphanstate1.append("Y")
                        childlessstate1.append("Y")
                if len(state1) > 1:
                    self.drawFSM(state1, orphanstate1, childlessstate1, condition[i], action, agent, preconcept, precondition, postconcept, postcondition,
                            files)
                state1 = []
                state1.append("unknown")
                orphanstate1 = []
                orphanstate1.append("*")
                childlessstate1 = []
                childlessstate1.append("*")
                for k in range(0, len(state)):
                    present = False
                    for j in range(0, len(state1)):
                        if state[k] == state1[j]:
                            present = True
                    if present == False:
                        state1.append(state[k])
                        orphanstate1.append("Y")
                        childlessstate1.append("Y")
                if len(state1) > 1:
                    self.drawFSMXML(state1, orphanstate1, childlessstate1, condition[i], action, agent, preconcept, precondition, postconcept, postcondition,
                            files)

        if self.var5.get() == 1:
            self.drawUseCase(agent, action, object, files)
            self.drawUseCaseXML(agent, action, object, files)

        if len(files) == 0:
            self.text_0.insert(END, "\n" + "No conceptual models were selected to be generated!" + "\n")
            self.text_0.see(END)
        else:
            self.text_0.insert(END, "\n" + "The following diagrams were generated..." + "\n")
            self.text_0.see(END)
            for j in range(0, len(files)):
                self.text_0.insert(END, "\n" + str(j + 1) + ". " + files[j])
                self.text_0.see(END)
        turtle.bye()
        messagebox.showinfo("Conceptual Model Tool", "Conceptual Model(s) generated successfully!")
        self.text_0.insert(END, "\n\nConceptual Model(s) generated successfully!\n\n")
        self.text_0.see(END)
        root.destroy()

    # -------------------------------------------------------------------------------------------
    # Precondition Symbol
    # -------------------------------------------------------------------------------------------

    def preconditionsymbol(self, action, preconcept, precondition, postconcept, postcondition, preconcepttype):

        count = 0
        actionbkup = []
        for i in range(0, len(preconcept)):
            if i > 0:
                if action[i] != action[i-1]:
                    count = 0
                    actionbkup = []
            for j in range(0, len(preconcept)):
                if i != j and (action[j] not in actionbkup) and preconcept[i] == postconcept[j] and precondition[i] == postcondition[j]:
                    count = count + 1
                    actionbkup.append(action[j])
            if count > 1:
                preconcepttype[i] = "[o]"
        for i in range(1, len(preconcept)):
            if action[i] == action [i-1]:
                if preconcepttype[i] == "[x]" or preconcepttype[i] == "[+]":
                    if preconcepttype[i-1] == "[o]" or preconcepttype[i-1] == "":
                        preconcepttype[i-1] = preconcepttype[i]
                if preconcepttype[i-1] == "[x]" or preconcepttype[i-1] == "[+]":
                    if preconcepttype[i] == "[o]" or preconcepttype[i] == "":
                        preconcepttype[i] = preconcepttype[i-1]
                if preconcepttype[i] == "[o]":
                    if preconcepttype[i-1] == "":
                        preconcepttype[i-1] = preconcepttype[i]
                if preconcepttype[i-1] == "[o]":
                    if preconcepttype[i] == "":
                        preconcepttype[i] = preconcepttype[i-1]

    # -------------------------------------------------------------------------------------------
    # Postcondition Symbol
    # -------------------------------------------------------------------------------------------

    def postconditionsymbol(self, preconcept, precondition, postconcept, postcondition, postconcepttype):

        for i in range(0, len(postconcept)):
            count = 0
            for j in range(0, len(postconcept)):
                if i != j and postconcept[i] == preconcept[j] and postcondition[i] == precondition[j]:
                    count = count + 1
            if count > 1:
                postconcepttype[i] = "[o]"

    # -------------------------------------------------------------------------------------------
    # Validate Table
    # -------------------------------------------------------------------------------------------
    def validateTable(self,agent, action, object, preconcept, precondition, postconcept, postcondition):

        validity = True

        tempconcept = ""
        tempcondition = ""

        for i in range(0, len(agent)):
            if preconcept[i] != postconcept[i]:
                for j in range(i + 1, len(agent)):
                    if agent[i] == agent[j] and action[i] == action[j] and object[i] == object[j] and preconcept[i] == postconcept[j]:
                        tempconcept = postconcept[i]
                        postconcept[i] = postconcept[j]
                        postconcept[j] = tempconcept
                        tempcondition = postcondition[i]
                        postcondition[i] = postcondition[j]
                        postcondition[j] = tempcondition

        for i in range(0, len(agent)):

            # agent[i] = self.spellCheck(agent[i])
            # action[i] = self.spellCheck(action[i])
            # object[i] = self.spellCheck(object[i])
            # preconcept[i] = self.spellCheck(preconcept[i])
            # precondition[i] = self.spellCheck(precondition[i])
            # postconcept[i] = self.spellCheck(postconcept[i])
            # postcondition[i] = self.spellCheck(postcondition[i])

            if preconcept[i] == postconcept[i] and precondition[i] == postcondition[i]:
                self.text_0.insert(END, "\n" + "ERROR: pre- & post-conditions are same (" + preconcept[i] + " = " + precondition[
                    i] + ") for user story where " + agent[i] + " attempts to " + action[i] + "!" + "\n")
                self.text_0.see(END)
                validity = False

            for j in range(0, i):
                if agent[i] == agent[j] and action[i] == action[j] and object[i] == object[j] and preconcept[i] == \
                        preconcept[j] and postconcept[i] == postconcept[j] and precondition[i] == precondition[j] and \
                        postcondition[i] == postcondition[j]:
                    self.text_0.insert(END, "\n" + "ERROR: duplicate user story - " + agent[i] + " " + action[i] + " " + object[i] + "!" + "\n")
                    self.text_0.see(END)
                    validity = False

                if agent[i] == agent[j] and action[i] == action[j] and object[i] == object[j] and preconcept[i] == \
                        preconcept[j] and postconcept[i] == postconcept[j] and precondition[i] == precondition[j] and \
                        postcondition[i] != postcondition[j]:
                    self.text_0.insert(END, "\n" + "ERROR: conflicting user stories - for " + agent[i] + " " + action[i] + " " + object[
                        i] + ", post-condition is " + postconcept[i] + " = " + postcondition[i] + " and " + postconcept[
                              i] + " = " + postcondition[j] + "!" + "\n")
                    self.text_0.see(END)
                    validity = False

        return validity

    # -------------------------------------------------------------------------------------------
    # Spell Check
    # -------------------------------------------------------------------------------------------
    def spellCheck(self,mystring):
        myarray = []
        myarray = mystring.split(" ")
        outstring = ""
        for i  in range(0,len(myarray)):
            if i == 0:
                outstring = spell(myarray[i])
            else:
                outstring = outstring + " " + spell(myarray[i])
        return outstring


    # -------------------------------------------------------------------------------------------
    # Draw Rectangle
    # -------------------------------------------------------------------------------------------

    def drawRectangle(self, x, y, l1, l2, text1,text2,text3,text4):

        turtle.hideturtle()
        turtle.speed(0)
        turtle.penup()
        turtle.goto(x - l1 / 2, y + l2 / 2)
        turtle.pendown()
        turtle.begin_fill()
        turtle.color("black")
        turtle.forward(l1)
        turtle.right(90)
        turtle.forward(l2)
        turtle.right(90)
        turtle.forward(l1)
        turtle.right(90)
        turtle.forward(l2)
        turtle.right(90)
        turtle.color("white")
        turtle.end_fill()
        self.writeText(x - 2 * len(text1) - 5, y - 5, text1)
        self.writeText(x - 2 * len(text2) - 5, y - 20, text2)
        self.writeText(x - 45, y + 20, text3)
        self.writeText(x + 35, y + 20, text4)

    # -------------------------------------------------------------------------------------------
    # Draw Circle
    # -------------------------------------------------------------------------------------------

    def drawCircle(self, x, y, r, text):

        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x, y - 20)
        turtle.pendown()
        turtle.setheading(0)
        turtle.begin_fill()
        turtle.circle(r)
        turtle.color("white")
        turtle.end_fill()
        self.writeText(x - 2 * len(text) - 5, y + 3, text)
        turtle.penup()

    # -------------------------------------------------------------------------------------------
    # Draw Arc
    # -------------------------------------------------------------------------------------------

    def drawArc(self, x, y, r, angle, direction, text):

        turtle.shape("classic")
        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x, y - 20)
        turtle.pendown()
        turtle.setheading(direction)
        turtle.circle(r, angle)
        turtle.stamp()
        self.writeText(x - 2 * len(text) - 5, y + 3, text)
        turtle.penup()

    # -------------------------------------------------------------------------------------------
    # Draw Ellipse
    # -------------------------------------------------------------------------------------------

    def drawEllipse(self, l, w):
        turtle.penup()
        turtle.forward(w * 8)
        turtle.left(90)
        turtle.forward(5)
        turtle.right(90)
        turtle.pendown()
        turtle.shape("circle")
        turtle.shapesize(l, w, 1)
        turtle.fillcolor("white")
        turtle.stamp()

    # -------------------------------------------------------------------------------------------
    # Draw Human
    # -------------------------------------------------------------------------------------------

    def drawHuman(self, x, y, text):
        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.circle(5)
        turtle.penup()
        turtle.left(270)
        turtle.pendown()
        turtle.forward(10)
        turtle.penup()
        turtle.left(45)
        turtle.pendown()
        turtle.forward(10)
        turtle.penup()
        turtle.backward(10)
        turtle.right(90)
        turtle.pendown()
        turtle.forward(10)
        turtle.penup()
        turtle.right(135)
        turtle.forward(13)
        turtle.right(90)
        turtle.pendown()
        turtle.forward(14)
        turtle.penup()
        turtle.backward(14)
        turtle.right(90)
        turtle.forward(20)
        turtle.left(90)
        self.writeText(x - 2 * len(text) - 5, y - 40, text)
    # -------------------------------------------------------------------------------------------
    # Draw Diamond
    # -------------------------------------------------------------------------------------------

    def drawDiamond(self, x, y, l1, l2, text):

        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.left(45)
        turtle.forward(l1)
        turtle.right(90)
        turtle.forward(l2)
        turtle.right(90)
        turtle.forward(l1)
        turtle.right(90)
        turtle.forward(l2)
        turtle.right(90)
        self.writeText(x + (l1 - 4 * len(text) + l1 / 2) / 2, y, text)

    # -------------------------------------------------------------------------------------------
    # Draw Line
    # -------------------------------------------------------------------------------------------

    def drawLine(self,x1, y1, x2, y2):

        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.goto(x2, y2)
        turtle.penup()

    # -------------------------------------------------------------------------------------------
    # Draw Arrow for FSM
    # -------------------------------------------------------------------------------------------

    def drawArrowFSM(self, x1, y1, x2, y2, text):

        rand1 = random.randint(-5, 5)
        rand2 = random.randint(-5, 5)
        rand3 = random.randint(-20, 20)
        rand4 = random.randint(-20, 20)

        turtle.shape("classic")
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x1 + rand1, y1 + rand2)
        turtle.pendown()
        turtle.goto(x2 + rand1, y2 + rand2)
        turtle.left(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        turtle.stamp()
        turtle.penup()
        turtle.right(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        self.writeText(5 + (x1 + 3 * x2) / 4 + rand3, 5 + (y1 + 3 * y2) / 4 + rand4, text)


    # -------------------------------------------------------------------------------------------
    # Draw Arrow for BPMN
    # -------------------------------------------------------------------------------------------

    def drawArrowBPMN(self, x1, y1, x2, y2, xpos1, ypos1, xpos2, ypos2, size):

        rand1 = random.randint(-1500, 1500)
        rand2 = random.randint(-1500, 1500)

        rand1 = rand1 / 100
        rand2 = rand2 / 100

        turtle.shape("classic")
        turtle.shapesize(size,size,size)
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        if xpos1 == xpos2 and ypos2 == ypos1 + 1:
            turtle.goto(x1 + 50, y1)
            turtle.pendown()
            turtle.goto(x2 - 50, y2)
            turtle.left(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        elif xpos1 == xpos2 and ypos1 == ypos2 + 1:
            turtle.goto(x1 - 50, y1)
            turtle.pendown()
            turtle.goto(x2 + 50, y2)
            turtle.left(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        elif ypos1 == ypos2 and xpos2 == xpos1 + 1:
            turtle.goto(x1, y1 - 37.5)
            turtle.pendown()
            turtle.goto(x2, y2 + 37.5)
            turtle.left(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        elif ypos1 == ypos2 and xpos1 == xpos2 + 1:
            turtle.goto(x1, y1 + 37.5)
            turtle.pendown()
            turtle.goto(x2, y2 - 37.5)
            turtle.left(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi)
        elif ypos2 == ypos1 + 1:
            turtle.goto(x1 + 50, y1 + rand1)
            turtle.pendown()
            turtle.goto(x1 + 75, y1 + rand1)
            turtle.right(90)
            turtle.goto(x1 + 75, y2 + rand2)
            turtle.left(90)
            turtle.goto(x2 - 50, y2 + rand2)
            turtle.left(math.atan2(0, (x2 - x1 + 25)) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2(0, (x2 - x1 + 25)) * 180 / math.pi)
        elif xpos2 == xpos1 + 1:
            turtle.goto(x1 + rand1, y1 - 37.5)
            turtle.pendown()
            turtle.goto(x1 + rand1, y1 - 62.5)
            turtle.left(90)
            turtle.goto(x2 + rand2, y1 - 62.5)
            turtle.right(90)
            turtle.goto(x2 + rand2, y2 + 37.5)
            turtle.left(math.atan2((y2 - y1 - 100), 0) * 180 / math.pi)
            turtle.stamp()
            turtle.penup()
            turtle.right(math.atan2((y2 - y1 - 100), 0) * 180 / math.pi)
        else:
            turtle.goto(x1 + rand1, y1 - 37.5)
            turtle.pendown()
            turtle.goto(x1 + rand1, y1 - 62.5 + rand2)
            turtle.left(90)
            turtle.goto(x2 - 75 + rand2, y1 - 62.5 + rand2)
            turtle.right(90)
            turtle.goto(x2 - 75 + rand2, y2 + rand1)
            turtle.left(90)
            turtle.goto(x2 - 50, y2 + rand1)
            turtle.left(-90)
            turtle.stamp()
            turtle.penup()

    # -------------------------------------------------------------------------------------------
    # Write Text in Graph
    # -------------------------------------------------------------------------------------------

    def writeText(self, x, y, text):

        turtle.hideturtle()
        turtle.speed(0)
        turtle.color("black")
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.write(text, move=False, font=("Arial", 12, "normal"))
        turtle.penup()

    # -------------------------------------------------------------------------------------------
    # Save Picture
    # -------------------------------------------------------------------------------------------

    def savePicture(self,path):

        ts = turtle.getscreen()
        ts.getcanvas().postscript(file=path)

    # -------------------------------------------------------------------------------------------
    # Create Domain Model XML
    # -------------------------------------------------------------------------------------------

    def drawDomainXML(self, agent, action, object, files):

        self.text_0.insert(END, "\nCreating Domain XML...\n")
        self.text_0.see(END)
        agentunique = []
        actionunique = []
        objectunique = []

        entity = []

        f = open(root.filelocation + "\\DOMAIN.xml", 'w+')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<domain xmlns="https://www.w3schools.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://www.w3schools.com domain.xsd">' + "\n")

        for i in range(0,len(action)):
            indicator = False
            for j in range(0,len(actionunique)):
                if action[i] == actionunique[j] and agent[i] == agentunique[j] and object[i] == objectunique[j]:
                    indicator = True
            if indicator == False:
                agentunique.append(agent[i])
                actionunique.append(action[i])
                objectunique.append(object[i])

        for i in range(0,len(agentunique)):
            indicator = False
            for j in range(0,len(entity)):
                if agentunique[i] == entity[j]:
                    indicator = True 
            if indicator == False:
                entity.append(agentunique[i])
                f.write("  <entity name=" + '"' + agentunique[i] + '"' + ">\n")
                f.write("    <type>agent</type>\n")
                f.write("  </entity>\n") 

        for i in range(0,len(objectunique)):
            indicator = False
            for j in range(0,len(entity)):
                if objectunique[i] == entity[j]:
                    indicator = True 
            if indicator == False:
                entity.append(objectunique[i])
                f.write("  <entity name=" + '"' + objectunique[i] + '"' + ">\n")
                f.write("    <type>object</type>\n")
                f.write("  </entity>\n") 

        for i in range(0,len(actionunique)):
            f.write("  <relationship name=" + '"' + actionunique[i] + '"' + ">\n")  
            f.write("    <agent>" + agentunique[i] + "</agent>\n")
            f.write("    <object>" + objectunique[i] + "</object>\n")
            f.write("  </relationship>\n") 

        f.write("</domain>\n")
        f.close()

    # -------------------------------------------------------------------------------------------
    # Draw ER Diagram - All
    # -------------------------------------------------------------------------------------------

    def drawER(self, agent, action, object, files, suffix):

        size = 256
        self.text_0.insert(END, "\nCreating ER Diagram for " + suffix.title() + "...\n")
        self.text_0.see(END)
        concept = []
        conceptInd = []

        concept_x = []
        concept_y = []

        for i in range(0, len(agent)):
            present = False
            for j in range(0, len(concept)):
                if agent[i] == concept[j]:
                    present = True
            if present == False:
                concept.append(agent[i])
                conceptInd.append("*")

        for i in range(0, len(object)):
            present = False
            for j in range(0, len(concept)):
                if object[i] == concept[j] and conceptInd[j] == "":
                    present = True
            if present == False:
                concept.append(object[i])
                conceptInd.append("")

        turtle.screensize(canvwidth=None, canvheight=None, bg=None)

        self.writeText(-350, 300, "DOMAIN MODEL - " + suffix.upper())
        self.writeText(-350, 280, "(Legend: * = agent)")

        radius = size
        increment = 2 * math.pi / len(concept)
        theta = 0
        x = 0
        y = size

        for j in range(0, len(concept)):
            concept_x.append(x)
            concept_y.append(y)
            theta = math.atan2(y, x)
            x = radius * math.cos(theta - increment)
            y = radius * math.sin(theta - increment)

        agent1 = []
        action1 = []
        object1 = []

        tempaction = ""
        tempobject = ""

        for i in range(0, len(action)):
            present = False
            if i == 0:
                tempaction = ""
                tempobject = ""
            else:
                tempaction = action[i - 1]
                tempobject = object[i - 1]
            if action[i] != tempaction or object[i] != tempobject:
                for j in range(0, len(action1)):
                    if agent[i] == agent1[j] and object[i] == object1[j] and action[i] != action[i - 1]:
                        action1[j] = action1[j] + ", " + action[i]
                        present = True
                if present == False:
                    agent1.append(agent[i])
                    action1.append(action[i])
                    object1.append(object[i])

        for i in range(0, len(action1)):
            for j in range(0, len(concept)):
                if agent1[i] == concept[j] and conceptInd[j] == "*":
                    entity1 = j
                if object1[i] == concept[j] and conceptInd[j] == "":
                    entity2 = j
            self.drawLine(concept_x[entity1], concept_y[entity1], concept_x[entity2], concept_y[entity2])

        radius = size
        increment = 2 * math.pi / len(concept)
        theta = 0
        x = 0
        y = size

        for j in range(0, len(concept)):
            self.drawRectangle(x, y, 100, 75, concept[j] + conceptInd[j],"","","")
            theta = math.atan2(y, x)
            x = radius * math.cos(theta - increment)
            y = radius * math.sin(theta - increment)

        for i in range(0, len(action1)):
            for j in range(0, len(concept)):
                if agent1[i] == concept[j]:
                    entity1 = j
                if object1[i] == concept[j]:
                    entity2 = j
            self.writeText((concept_x[entity1] + 3 * concept_x[entity2]) / 4, (concept_y[entity1] + 3 * concept_y[entity2]) / 4,
                      action1[i])

        self.savePicture(root.filelocation + "\\ERD - " + suffix.upper() + ".eps")
        turtle.clear()
        files.append("ERD - " + suffix.upper() + ".eps")

    # -------------------------------------------------------------------------------------------
    # Create Use Case XML
    # -------------------------------------------------------------------------------------------

    def drawUseCaseXML(self, agent, action, object, files):

        self.text_0.insert(END, "\nCreating Use Case XML...\n")
        self.text_0.see(END)
        agentunique = []
        actionunique = []
        objectunique = []

        actor = []

        f = open(root.filelocation + "\\USE CASE.xml", 'w+')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<usecasemodel xmlns="https://www.w3schools.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://www.w3schools.com domain.xsd">' + "\n")

        for i in range(0,len(action)):
            indicator = False
            for j in range(0,len(actionunique)):
                if action[i] == actionunique[j] and agent[i] == agentunique[j] and object[i] == objectunique[j]:
                    indicator = True
            if indicator == False:
                agentunique.append(agent[i])
                actionunique.append(action[i])
                objectunique.append(object[i])

        for i in range(0,len(agentunique)):
            indicator = False
            for j in range(0,len(actor)):
                if agentunique[i] == actor[j]:
                    indicator = True 
            if indicator == False:
                actor.append(agentunique[i])
                f.write("  <actor name=" + '"' + agentunique[i] + '"' + "/>\n")

        for i in range(0,len(actionunique)):
            f.write("  <usecase name=" + '"' + actionunique[i] + " " + objectunique[i] + '"' + ">\n")  
            f.write("    <actor>" + agentunique[i] + "</actor>" + "\n")
            f.write("  </usecase>\n") 

        f.write("</usecasemodel>\n")
        f.close()

    # -------------------------------------------------------------------------------------------
    # Draw Use Case Diagram
    # -------------------------------------------------------------------------------------------

    def drawUseCase(self, agent, action, object, files):

        self.text_0.insert(END, "\nCreating Use Case Diagram...\n")
        self.text_0.see(END)
        agentunique = []
        actionunique = []
        objectunique = []

        for i in range(0,len(action)):
            indicator = False
            for j in range(0,len(actionunique)):
                if action[i] == actionunique[j] and agent[i] == agentunique[j] and object[i] == objectunique[j]:
                    indicator = True
            if indicator == False:
                agentunique.append(agent[i])
                actionunique.append(action[i])
                objectunique.append(object[i])

        agentfreq = []
        frequency = []

        for i in range(0, len(actionunique)):
            indicator = False
            for j in range(0,len(agentfreq)):
                if agentunique[i] == agentfreq[j]:
                    frequency[j] = frequency[j] + 1
                    indicator = True
            if indicator == False:
                agentfreq.append(agentunique[i])
                frequency.append(1)

        index = frequency.index(max(frequency))

        agent1 = []
        agent2 = []
        agent1counter = 0
        agent2counter = 0

        for i in range(0,len(agentfreq)):
            index = frequency.index(max(frequency))
            if agent1counter <= agent2counter:
                agent1.append(agentfreq[index])
                agent1counter = agent1counter + frequency[index]
            else:
                agent2.append(agentfreq[index])
                agent2counter = agent2counter + frequency[index]
            frequency[index] = -1

        self.writeText(-350, 300, "USE CASE")

        position1 = 0
        position2 = 0

        for i in range(0,len(agentunique)):
            for j in range(0,len(agent1)):
                if agentunique[i] == agent1[j]:
                    position1 = position1 + 1
            for j in range(0,len(agent2)):
                if agentunique[i] == agent2[j]:
                    position2 = position2 + 1

        increment = 500/(max(position1,position2))

        position1 = 0
        position2 = 0

        agent1list = []
        agent2list = []

        agent1position = []
        agent2position = []

        for j in range(0,len(agent1)):
            for i in range(0, len(agentunique)):
                if agentunique[i] == agent1[j]:
                    position1 = position1 + 1
                    agent1list.append(agentunique[i])
                    agent1position.append(position1 * increment - 310)

        for j in range(0, len(agent2)):
            for i in range(0, len(agentunique)):
                if agentunique[i] == agent2[j]:
                    position2 = position2 + 1
                    agent2list.append(agentunique[i])
                    agent2position.append(position2 * increment - 310)

        agentbackup = ""
        sum = 0
        count = 0

        agent1location = []
        user = []

        for i in range(0,len(agent1position)):
            if agent1list[i] == agentbackup or agentbackup == "":
                sum = sum + agent1position[i]
                count = count + 1
            else:
                agent1location.append(sum/count)
                user.append(agentbackup)
                sum = 0
                count = 0
                sum = sum + agent1position[i]
                count = count + 1
            agentbackup = agent1list[i]
        agent1location.append(sum / count)
        user.append(agentbackup)

        for i in range(0,len(agent1)):
            self.drawHuman(-300, agent1location[i], user[i])

        for i in range(0,len(agent1location)):
            for j in range(0,len(agent1position)):
                if user[i] == agent1list[j]:
                    self.drawLine(-285, agent1location[i], -125, agent1position[j])

        agentbackup = ""
        sum = 0
        count = 0

        agent2location = []
        user = []

        for i in range(0,len(agent2position)):
            if agent2list[i] == agentbackup or agentbackup == "":
                sum = sum + agent2position[i]
                count = count + 1
            else:
                agent2location.append(sum/count)
                user.append(agentbackup)
                sum = 0
                count = 0
                sum = sum + agent2position[i]
                count = count + 1
            agentbackup = agent2list[i]
        if count > 0:
            agent2location.append(sum / count)
            user.append(agentbackup)

        for i in range(0,len(agent2)):
            self.drawHuman(300, agent2location[i], user[i])

        for i in range(0,len(agent2location)):
            for j in range(0,len(agent2position)):
                if user[i] == agent2list[j]:
                    self.drawLine(75, agent2position[j], 285, agent2location[i])

        position1 = 0
        position2 = 0

        for j in range(0, len(agent1)):
            for i in range(0,len(agentunique)):
                if agentunique[i] == agent1[j]:
                    position1 = position1 + 1
                    self.writeText(-150, position1 * increment - 325, "")
                    self.drawEllipse(2, len(actionunique[i] + " " + objectunique[i])/3)
                    self.writeText(-150, position1 * increment - 325, actionunique[i] + " " + objectunique[i])

        for j in range(0, len(agent2)):
            for i in range(0, len(agentunique)):
                if agentunique[i] == agent2[j]:
                    position2 = position2 + 1
                    self.writeText(50, position2 * increment - 325, "")
                    self.drawEllipse(2,len(actionunique[i] + " " + objectunique[i])/3)
                    self.writeText(50, position2 * increment - 325, actionunique[i] + " " + objectunique[i])

        self.savePicture(root.filelocation + "\\USE CASE DIAGRAM.eps")
        turtle.clear()
        files.append("USE CASE DIAGRAM.eps")

    # -------------------------------------------------------------------------------------------
    # Create Process Model XML
    # -------------------------------------------------------------------------------------------

    def drawProcessModelXML(self, agent, action, object, preconcept, precondition, postconcept, postcondition, preconcepttype, postconcepttype, files):

        self.text_0.insert(END, "\nCreating Process Model XML...\n")
        self.text_0.see(END)
        agentunique = []
        actionunique = []
        objectunique = []

        actor = []

        f = open(root.filelocation + "\\PROCESS MODEL.xml", 'w+')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<process xmlns="https://www.w3schools.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://www.w3schools.com domain.xsd">' + "\n")

        for i in range(0,len(action)):
            indicator = False
            for j in range(0,len(actionunique)):
                if action[i] == actionunique[j] and agent[i] == agentunique[j] and object[i] == objectunique[j]:
                    indicator = True
            if indicator == False:
                agentunique.append(agent[i])
                actionunique.append(action[i])
                objectunique.append(object[i])

        for i in range(0,len(agentunique)):
            indicator = False
            for j in range(0,len(actor)):
                if agentunique[i] == actor[j]:
                    indicator = True 
            if indicator == False:
                actor.append(agentunique[i])
                f.write("  <swimlane name=" + '"' + agentunique[i] + '"' + "/>\n")

        for i in range(0,len(actionunique)):
            f.write("  <activity name=" + '"' + actionunique[i] + " " + objectunique[i] + '"' + ">\n")  
            f.write("    <swimlane>" + agentunique[i] + "</swimlane>" + "\n")
            indicator1 = 1
            for j in range(0,len(agentunique)):
                if postconcept[j] == preconcept[i] and postcondition[j] == precondition[i]: 
                    indicator1 = 0
            f.write("    <isinitial>" + str(indicator1) + "</isinitial>" + "\n")
            indicator2 = 1
            for j in range(0,len(agent)):
                if postconcept[i] == preconcept[j] and postcondition[i] == precondition[j]: 
                    indicator2 = 0
            f.write("    <isfinal>" + str(indicator2) + "</isfinal>" + "\n")
            f.write("    <precondition>" + preconcepttype[i] + "</precondition>" + "\n")
            f.write("    <postcondition>" + postconcepttype[i] + "</postcondition>" + "\n")
            f.write("  </activity>\n") 

        for i in range(0,len(agent)):
            for j in range(0,len(agent)):
                if postconcept[i] == preconcept[j] and postcondition[i] == precondition[j]: 
                    f.write("  <dependency>\n") 
                    f.write("    <fromactivity>" + action[i] + " " + object[i] + "</fromactivity>" + "\n") 
                    f.write("    <toactivity>" + action[j] + " " + object[j] + "</toactivity>" + "\n") 
                    f.write("  </dependency>\n") 
        f.write("</process>\n")
        f.close()


    # -------------------------------------------------------------------------------------------
    # Draw BPMN Diagram
    # -------------------------------------------------------------------------------------------

    def drawBPMN(self, agent, action, object, preconcept, precondition, postconcept, postcondition, preconcepttype, postconcepttype, files):

        self.text_0.insert(END, "\nCreating BPMN Diagram...\n")
        self.text_0.see(END)
        action_x = []
        action_y = []
        action_name = []
        agent_name = []
        object_name = []

        box_x = []
        box_y = []

        y = 340

        agentcount = 0

        turtle.speed(0)
        turtle.hideturtle()
        self.writeText(-700, 300, "PROCESS MODEL")
        self.writeText(-700, 280, "(Legend: [o] = or, [+] = and, [x] = exclusive or)")
        turtle.penup()
        turtle.goto(-750, 275)
        for k in range(-50, 90):
            turtle.pendown()
            turtle.forward(5)
            turtle.penup()
            turtle.forward(5)

        for i in range(0, len(agent)):

            duplicate = False
            for j in range(0, i):
                if agent[i] == agent[j]:
                    duplicate = True
            if duplicate == False:
                tempaction = []
                tempagent = []
                tempobject = []
                temppreconcepttype = []
                temppostconcepttype = []
                tempaction.append(action[i])
                tempagent.append(agent[i])
                tempobject.append(object[i])
                temppreconcepttype.append(preconcepttype[i])
                temppostconcepttype.append(postconcepttype[i])

                agentcount = agentcount + 1
                actioncount = 0

                for j in range(0, len(agent)):
                    if agent[i] == agent[j] and i != j and action[j] != action[j - 1]:
                        tempaction.append(action[j])
                        tempagent.append(agent[j])
                        tempobject.append(object[j])
                        temppreconcepttype.append(preconcepttype[j])
                        temppostconcepttype.append(postconcepttype[j])

                x = -700
                y = y - 125
                self.writeText(-750, y - 5, agent[i])
                turtle.speed(0)
                turtle.goto(-750,y - 57.5)
                for k in range(-50,90):
                    turtle.pendown()
                    turtle.forward(5)
                    turtle.penup()
                    turtle.forward(5)

                for j in range(0, len(tempaction)):
                    x = x + 150
                    actioncount = actioncount + 1
                    self.drawRectangle(x, y, 100, 75, tempaction[j], tempobject[j], temppreconcepttype[j],temppostconcepttype[j])
                    startindicator = True
                    endindicator = True
                    for k in range(0,len(agent)):
                        if tempagent[j] == agent[k] and tempaction[j] == action[k] and tempobject[j] == object[k]:
                            for l in range(0, len(agent)):
                                #if k > l and preconcept[k] == postconcept[l] and precondition[k] == postcondition[l]:
                                if preconcept[k] == postconcept[l] and precondition[k] == postcondition[l]:
                                    startindicator = False
                                #if k < l and postconcept[k] == preconcept[l] and postcondition[k] == precondition[l]:
                                if postconcept[k] == preconcept[l] and postcondition[k] == precondition[l]:
                                    endindicator = False
                    if startindicator == True:
                        self.drawCircle(x - 65, y + 15, 5, "")
                        self.drawLine(x - 50, y, x - 60, y)
                    if endindicator == True:
                        self.drawCircle(x + 65, y + 15, 5, "")
                        self.drawLine(x + 50, y, x + 60, y)
                    action_x.append(x)
                    action_y.append(y)
                    action_name.append(tempaction[j])
                    agent_name.append(tempagent[j])
                    object_name.append(tempobject[j])
                    box_x.append(agentcount)
                    box_y.append(actioncount)

        x_first_bkup = -999999
        y_first_bkup = -999999
        x_second_bkup = -999999
        y_second_bkup = -999999

        for i in range(0, len(agent)):
            #for j in range(0, i):
            for j in range(0, len(agent)):
                if preconcept[i] == postconcept[j] and precondition[i] == postcondition[j]:
                    for k in range(0, len(action_x)):
                        if action[j] == action_name[k] and agent[j] == agent_name[k] and object[j] == object_name[k]:
                            x_first = action_x[k]
                            y_first = action_y[k]
                            x1_first = box_x[k]
                            y1_first = box_y[k]
                        if action[i] == action_name[k] and agent[i] == agent_name[k] and object[i] == object_name[k]:
                            x_second = action_x[k]
                            y_second = action_y[k]
                            x1_second = box_x[k]
                            y1_second = box_y[k]

                    if x_first_bkup != x_first or y_first_bkup != y_first or x_second_bkup != x_second or y_second_bkup != y_second:
                        self.drawArrowBPMN(x_first, y_first, x_second, y_second, x1_first, y1_first, x1_second, y1_second, 1)
                        x_first_bkup = x_first
                        y_first_bkup = y_first
                        x_second_bkup = x_second
                        y_second_bkup = y_second

        self.savePicture(root.filelocation + "\\BPMN DIAGRAM.eps")
        turtle.clear()
        files.append("BPMN DIAGRAM.eps")

    # -------------------------------------------------------------------------------------------
    # Create FSM XML
    # -------------------------------------------------------------------------------------------

    def drawFSMXML(self, state, orphanstate, childlessstate, object, action, agent, preconcept, precondition, postconcept, postcondition, files):

        self.text_0.insert(END, "\nCreating FSM XML for " + object.title() + "...\n")
        self.text_0.see(END)

        transition = []
        byactor = []
        fromstate = []
        tostate = []

        f = open(root.filelocation + "\\STATE MACHINE.xml", 'w+')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<statemachine xmlns="https://www.w3schools.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" objectname=' + '"' + object + '"' + ' xsi:schemaLocation="https://www.w3schools.com domain.xsd">' + "\n")

        for j in range(0, len(state)):
            for i in range(0, len(state)):
                for k in range(0, len(action)):
                    if preconcept[k] == object and postconcept[k] == object and precondition[k] == state[j] and postcondition[k] == state[i]:
                        #self.drawStateTransition(state_x[j], state_y[j], state_x[i], state_y[i], action[k] + " (by " + agent[k] + ")")
                        transition.append(action[k])
                        byactor.append(agent[k])
                        fromstate.append(state[j])
                        tostate.append(state[i])
                        if i > 1:
                            orphanstate[i] = "N"

        for w in range(0, len(state)):
            if orphanstate[w] == "Y" or orphanstate[w] == "*":
                for x in range(0, len(agent)):
                    if state[w] == postcondition[x] and postconcept[x] == object:
                        #self.drawStateTransition(state_x[0], state_y[0], state_x[w], state_y[w], action[x] + " (by " + agent[x] + ")")
                        transition.append(action[x])
                        byactor.append(agent[x])
                        fromstate.append("unknown")
                        tostate.append(state[w])
                        orphanstate[w] = "N"
                        break

        for w in range(0, len(state)):
            if orphanstate[w] == "Y":
                for x in range(0, len(agent)):
                    if state[w] == precondition[x] and preconcept[x] == object:
                        #self.drawStateTransition(state_x[0], state_y[0], state_x[w], state_y[w], WordNetLemmatizer().lemmatize(state[w],'v') + " (precondition)")
                        transition.append("precondition")
                        byactor.append("")
                        fromstate.append("unknown")
                        tostate.append(state[w])
                        orphanstate[w] = "N"
                        break

        for j in range(0, len(state)):
            for i in range(0, len(state)):
                for k in range(0, len(action)):
                    if postconcept[k] == object and preconcept[k] == object and postcondition[k] == state[i] and precondition[k] == state[j]:
                        childlessstate[j] = "N"

        for j in range(0, len(state)):
            f.write("  <state name=" + '"' + state[j] + '"' + ">\n")
            if orphanstate[j] == "Y" or state[j] == "unknown":
                f.write("    <isinitial>1</isinitial>\n")
            else:
                f.write("    <isinitial>0</isinitial>\n")

            if childlessstate[j] == "Y":
                f.write("    <isfinal>1</isfinal>\n")
            else:
                f.write("    <isfinal>0</isfinal>\n")

            f.write("  </state>\n")

        for j in range(0, len(transition)):
            f.write("  <transition name=" + '"' + transition[j] + '"' + ">\n")
            f.write("    <by>" + byactor[j] + "</by>\n")
            f.write("    <fromstate>" + fromstate[j] + "</fromstate>\n")
            f.write("    <tostate>" + tostate[j] + "</tostate>\n")
            f.write("  </transition>\n")

        f.write("</statemachine>\n")
        f.close()


    # -------------------------------------------------------------------------------------------
    # Draw FSM Diagram
    # -------------------------------------------------------------------------------------------

    def drawFSM(self, state, orphanstate, childlessstate, object, action, agent, preconcept, precondition, postconcept, postcondition, files):

        self.text_0.insert(END, "\nCreating FSM Diagram for " + object.title() + "...\n")
        self.text_0.see(END)
        state_x = []
        state_y = []

        turtle.screensize(canvwidth=None, canvheight=None, bg=None)

        self.writeText(-350, 300, "STATE MACHINE - " + object.upper())
        self.writeText(-350, 280, "(Legend: (i) = initial state, double circle = final state)")

        radius = 256
        increment = 2 * math.pi / len(state)
        theta = 0
        x = 0
        y = 256

        for j in range(0, len(state)):
            self.drawCircle(x, y, 30, state[j])
            state_x.append(x)
            state_y.append(y)
            theta = math.atan2(y, x)
            x = radius * math.cos(theta - increment)
            y = radius * math.sin(theta - increment)

        for j in range(0, len(state)):
            for i in range(0, len(state)):
                for k in range(0, len(action)):
                    if preconcept[k] == object and postconcept[k] == object and precondition[k] == state[j] and postcondition[k] == state[i]:
                        self.drawStateTransition(state_x[j], state_y[j], state_x[i], state_y[i], action[k] + " (by " + agent[k] + ")")
                        if i > 1:
                            orphanstate[i] = "N"
                    else:
                        if self.var4A.get() == 1:
                            for l in range(0, len(action)):
                                if k != l:
                                    if preconcept[k] == object and postconcept[l] == object and postconcept[k] == preconcept[l] and postcondition[k] == precondition[l] and precondition[k] == state[j] and postcondition[l] == state[i] and state[i] != state[j]:
                                        self.drawStateTransition(state_x[j], state_y[j], state_x[i], state_y[i], action[k] + " (by " + agent[k] + ")" + " + " + action[l] + " (by " + agent[l] + ")")
                                        orphanstate[i] = "N"
                                    else:
                                        for m in range(0, len(action)):
                                            if m != k and m != l:
                                                if preconcept[k] == object and postconcept[l] == object and postconcept[k] == preconcept[m] and postcondition[k] == precondition[m] and postconcept[m] == preconcept[l] and postcondition[m] == precondition[l] and precondition[k] == state[j] and postcondition[l] == state[i] and state[i] != state[j]:
                                                    self.drawStateTransition(state_x[j], state_y[j], state_x[i], state_y[i], action[k] + " (by " + agent[k] + ")" + " + " + action[m] + " (by " + agent[m] + ")" + " + " + action[l] + " (by " + agent[l] + ")")
                                                    orphanstate[i] = "N"

        for w in range(0, len(state)):
            if orphanstate[w] == "Y":
                for x in range(0, len(agent)):
                    if state[w] == postcondition[x] and postconcept[x] == object:
                        self.drawStateTransition(state_x[0], state_y[0], state_x[w], state_y[w], action[x] + " (by " + agent[x] + ")")
                        orphanstate[w] = "N"
                        break

        for w in range(0, len(state)):
           if orphanstate[w] == "Y":
                for x in range(0, len(agent)):
                    if state[w] == precondition[x] and preconcept[x] == object:
                        self.drawStateTransition(state_x[0], state_y[0], state_x[w], state_y[w], WordNetLemmatizer().lemmatize(state[w],'v') + " (precondition)")
                        orphanstate[w] = "N"
                        break

        for j in range(0, len(state)):
            for i in range(0, len(state)):
                for k in range(0, len(action)):
                    if postconcept[k] == object and preconcept[k] == object and postcondition[k] == state[i] and precondition[k] == state[j]:
                        childlessstate[j] = "N"

        radius = 256
        increment = 2 * math.pi / len(state)
        theta = 0
        x = 0
        y = 256

        for j in range(0, len(state)):
            if childlessstate[j] == "Y":
               self.drawCircle(x, y+3.5, 26, state[j])
            state_x.append(x)
            state_y.append(y)
            theta = math.atan2(y, x)
            x = radius * math.cos(theta - increment)
            y = radius * math.sin(theta - increment)

        radius = 256
        increment = 2 * math.pi / len(state)
        theta = 0
        x = 0
        y = 256

        for j in range(0, len(state)):
            if orphanstate[j] != "N":
               #self.drawCircle(x, y+44.5, 5, "")
               self.writeText(x, y+20, "(i)")
            state_x.append(x)
            state_y.append(y)
            theta = math.atan2(y, x)
            x = radius * math.cos(theta - increment)
            y = radius * math.sin(theta - increment)

        self.savePicture(root.filelocation + "\\FSM - " + object.upper() + ".eps")
        turtle.clear()
        files.append("FSM - " + object.upper() + ".eps")

    # -------------------------------------------------------------------------------------------
    # Draw State Transitions in FSM Diagram
    # -------------------------------------------------------------------------------------------

    def drawStateTransition(self, xbackup, ybackup, x, y, text):

        theta1 = math.atan2(y - ybackup, x - xbackup)
        if ybackup == y:
            k = 1000000
        else:
            k = (x - xbackup) / (y - ybackup)

        if theta1 < math.pi and theta1 > 0:
            xnew1 = xbackup + 50 * k / math.sqrt(1 + k ** 2) + 5
            ynew1 = ybackup + 50 / math.sqrt(1 + k ** 2) - 5
            xnew2 = x - 50 * k / math.sqrt(1 + k ** 2) + 5
            ynew2 = y - 50 / math.sqrt(1 + k ** 2) - 4
        else:
            xnew1 = xbackup - 50 * k / math.sqrt(1 + k ** 2) - 5
            ynew1 = ybackup - 50 / math.sqrt(1 + k ** 2) + 5
            xnew2 = x + 50 * k / math.sqrt(1 + k ** 2) - 5
            ynew2 = y + 50 / math.sqrt(1 + k ** 2) + 5

        self.drawArrowFSM(xnew1, ynew1, xnew2, ynew2, text)

    def generate_model(self):
        self.extractComponents()


root = Tk()
root.minsize(600,250)
a = ResearchTool(root)
a.create_screen()
root.mainloop()
