# Copyright: Irmak Sirer 2011
#


import sys, time
import random as rnd
import numpy.random
poisson = numpy.random.poisson

from util import *
from layout import *
from AI import AI
from story import Story
from card import Character, Event, Support
from cardheap import Deck
import getDecision




# DEFINITIONS
class Game:
    def __init__(self, screen, Player1, Player2):
        self.screen = screen
        self.storydeck = []
        self.stories = [None, None, None]

        self.players = [Player1, Player2]
        self.P1 = self.Player1 = Player1
        self.P2 = self.Player2 = Player2
        Player1.game = self
        Player2.game = self
        Player1.position = "Player 1"
        Player2.position = "Player 2"
        Player1.screen = screen
        Player2.screen = screen

        self.P1domains = Player1.domains
        self.P1board = Player1.board
        self.P1discard = Player1.discardPile

        self.P2domains = Player2.domains
        self.P2board = Player2.board
        self.P2discard = Player2.discardPile

        self.winner = None

    #-- Reports
    def storyReport(self, showCommitted=False):
        report = reportColor('STORIES\n')
        if showCommitted:
            report += '\n'.join(map(lambda st: st.report(), self.stories)) + '\n'
        else:
            report += '\n'.join(map(repr, self.stories)) + '\n'
        return report

    def boardReport(self):
        return '\n'.join([self.Player2.boardReport(),
                          self.Player1.boardReport()])

    def report(self, showCommitted=False):
        return '\n'.join([self.Player2.boardReport(),
                          self.storyReport(showCommitted),
                          self.Player1.boardReport()])

    #-- Actions
    def drawStoryCard(self, storyslot):
        story = self.storydeck.pop()
        story.enterGame(self, storyslot)
        return story

    def initiateStories(self):
        self.drawStoryCard(0)
        self.drawStoryCard(1)
        self.drawStoryCard(2)

    def replace(self, story):
        story.uncommitAll()
        slot = self.stories.index(story)
        newStory = self.drawStoryCard(slot)
        self.drawStoryOnScreen(newStory, slot)
        newStory.drawCommitted(self.Player1)


    def win(self, player):
        self.winner = player
        print boldColor(player.name), printTurnHeader("WINS THE GAME!!!!!")
        self.screen.msgBox("%s wins the game!" % player.name)
        sys.exit() # REMOVE LATER!
    
    #-- Graphics
    def drawStoryOnScreen(self, story, slot):
        x = LEFTPANELWIDTH + self.spaceBetweenStories
        y = self.screen.height//2 - CARDWIDTH//2
        step = CARDHEIGHT + self.spaceBetweenStories
        pos = (x + slot*step, y)
        story.image.draw(pos)
        story.pos = pos
        story.spaceBetween = self.spaceBetweenStories

    def drawStories(self):
        storypanelwidth = self.screen.width - ZOOMEDCARDHEIGHT - LEFTPANELWIDTH
        space = (storypanelwidth - 3*CARDHEIGHT) // 4
        self.spaceBetweenStories = space
        x = LEFTPANELWIDTH + space
        y = self.screen.height//2 - CARDWIDTH//2
        step = CARDHEIGHT + space
        for i in range(3):
            pos = (x + i*(step), y)
            self.stories[i].image.draw(pos)
            self.stories[i].pos = pos
            self.stories[i].spaceBetween = space




class eachPlayerSacrificesOneCharAfterDraw(object):
    def hey():
        pass


def parseCardFile(cardFileName):
    cardOfType = {"Character": Character,
                  "Support":   Support,
                  "Event":     Event,
                  "Story":     Story}
    fields ={}
    # read file
    cardfile = open(cardFileName, 'r').readlines()
    for line in cardfile:
        if ':' in line and line[0] != '~':
            field, value = line.split(':',1)
            if value.strip() != "":
                fields[field] = value.strip()
    # create card
    name      = fields["Name"]
    cardtype  = fields["Type"]
    imageFile = "Images/" + fields["Image"]
    if cardtype not in cardOfType:
        raise GameError("Card type not recognized: %s" % cardtype)
    card = cardOfType[cardtype](name, imageFile)
    # put other info in
    card.faction = fields["Faction"]
    if "Cost" in fields:
        card.cost = int(fields["Cost"])
    if "Skill" in fields:
        card.printedSkill = card.skill = int(fields["Skill"])
    if "Icons" in fields:
        icons = fields["Icons"].lstrip('(').rstrip(')')
        for icon in icons.split(')('):
            if   icon == 'T':
                card.printedTerror += 1
                card.terror += 1
            elif icon == 'C':
                card.printedCombat += 1
                card.combat += 1
            elif icon == 'A':
                card.printedArcane += 1
                card.arcane += 1
            elif icon == 'I':
                card.printedInvestigation += 1
                card.investigation += 1
    if "Struggle Icons" in fields:
        card.struggles = []
        icons = fields["Struggle Icons"].lstrip('(').rstrip(')')
        for icon in icons.split(')('):
            if   icon == 'T':
                if cardtype == "Story":
                    card.appendTerrorStruggle()
            elif icon == 'C':
                if cardtype == "Story":
                    card.appendCombatStruggle()
            elif icon == 'A':
                if cardtype == "Story":
                    card.appendArcaneStruggle()
            elif icon == 'I':
                if cardtype == "Story":
                    card.appendInvestigationStruggle()
        if cardtype == "Story":
            card.appendSkillStruggle()
    if "Subtypes" in fields:
        card.subtypes = fields["Subtypes"].rstrip('.').split('.')
    if "Keywords" in fields:
        card.keywords = fields["Keywords"].rstrip('.').split('.')
    if "Set" in fields:
        card.set = fields["Set"]
    if "Number" in fields:
        card.number = int(fields["Number"])
    if "Actions" in fields:
        card.actions = map(eval, fields["Actions"].split(','))
    if "Disrupts" in fields:
        card.disrupts = map(eval, fields["Disrupts"].split(','))
    if "Responses" in fields:
        card.responses = map(eval, fields["Responses"].split(','))
    if "Forced Responses" in fields:
        try:
            card.forcedResponses = map(eval, fields["Forced Responses"].split(','))
        except:
            print fields["Forced Responses"]
            raise
    
    # return
    return card




