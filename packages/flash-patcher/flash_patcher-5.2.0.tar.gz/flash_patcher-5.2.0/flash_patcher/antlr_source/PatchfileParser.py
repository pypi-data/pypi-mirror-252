# Generated from ../flash_patcher/antlr_source/PatchfileParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,20,107,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,0,1,0,1,1,4,1,28,8,
        1,11,1,12,1,29,1,1,1,1,1,1,1,1,1,2,4,2,37,8,2,11,2,12,2,38,1,3,1,
        3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,4,5,52,8,5,11,5,12,5,53,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,7,4,7,67,8,7,11,7,12,7,68,
        1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,8,4,8,79,8,8,11,8,12,8,80,1,9,1,9,
        1,9,1,9,5,9,87,8,9,10,9,12,9,90,9,9,1,10,3,10,93,8,10,1,10,1,10,
        1,10,3,10,98,8,10,1,10,3,10,101,8,10,1,10,1,10,3,10,105,8,10,1,10,
        0,0,11,0,2,4,6,8,10,12,14,16,18,20,0,0,109,0,22,1,0,0,0,2,27,1,0,
        0,0,4,36,1,0,0,0,6,40,1,0,0,0,8,46,1,0,0,0,10,51,1,0,0,0,12,62,1,
        0,0,0,14,66,1,0,0,0,16,78,1,0,0,0,18,88,1,0,0,0,20,104,1,0,0,0,22,
        23,5,1,0,0,23,24,5,5,0,0,24,25,3,20,10,0,25,1,1,0,0,0,26,28,3,0,
        0,0,27,26,1,0,0,0,28,29,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,31,
        1,0,0,0,31,32,5,6,0,0,32,33,3,4,2,0,33,34,5,17,0,0,34,3,1,0,0,0,
        35,37,5,18,0,0,36,35,1,0,0,0,37,38,1,0,0,0,38,36,1,0,0,0,38,39,1,
        0,0,0,39,5,1,0,0,0,40,41,5,2,0,0,41,42,5,5,0,0,42,43,3,20,10,0,43,
        44,5,13,0,0,44,45,3,20,10,0,45,7,1,0,0,0,46,47,5,3,0,0,47,48,5,5,
        0,0,48,49,3,20,10,0,49,9,1,0,0,0,50,52,3,8,4,0,51,50,1,0,0,0,52,
        53,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,55,1,0,0,0,55,56,5,7,0,
        0,56,57,3,16,8,0,57,58,5,19,0,0,58,59,5,6,0,0,59,60,3,4,2,0,60,61,
        5,17,0,0,61,11,1,0,0,0,62,63,5,4,0,0,63,64,5,5,0,0,64,13,1,0,0,0,
        65,67,3,12,6,0,66,65,1,0,0,0,67,68,1,0,0,0,68,66,1,0,0,0,68,69,1,
        0,0,0,69,70,1,0,0,0,70,71,5,7,0,0,71,72,3,16,8,0,72,73,5,19,0,0,
        73,74,5,6,0,0,74,75,3,4,2,0,75,76,5,17,0,0,76,15,1,0,0,0,77,79,5,
        20,0,0,78,77,1,0,0,0,79,80,1,0,0,0,80,78,1,0,0,0,80,81,1,0,0,0,81,
        17,1,0,0,0,82,87,3,2,1,0,83,87,3,6,3,0,84,87,3,10,5,0,85,87,3,14,
        7,0,86,82,1,0,0,0,86,83,1,0,0,0,86,84,1,0,0,0,86,85,1,0,0,0,87,90,
        1,0,0,0,88,86,1,0,0,0,88,89,1,0,0,0,89,19,1,0,0,0,90,88,1,0,0,0,
        91,93,5,10,0,0,92,91,1,0,0,0,92,93,1,0,0,0,93,94,1,0,0,0,94,95,5,
        8,0,0,95,97,5,14,0,0,96,98,5,12,0,0,97,96,1,0,0,0,97,98,1,0,0,0,
        98,100,1,0,0,0,99,101,5,11,0,0,100,99,1,0,0,0,100,101,1,0,0,0,101,
        105,1,0,0,0,102,105,5,12,0,0,103,105,5,9,0,0,104,92,1,0,0,0,104,
        102,1,0,0,0,104,103,1,0,0,0,105,21,1,0,0,0,11,29,38,53,68,80,86,
        88,92,97,100,104
    ]

class PatchfileParser ( Parser ):

    grammarFileName = "PatchfileParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'('", "')'", "<INVALID>", 
                     "'-'" ]

    symbolicNames = [ "<INVALID>", "ADD", "REMOVE", "REPLACE", "REPLACE_ALL", 
                      "FILENAME", "BEGIN_PATCH", "BEGIN_CONTENT", "FUNCTION", 
                      "END", "OPEN_BLOCK", "CLOSE_BLOCK", "INTEGER", "DASH", 
                      "FUNCTION_NAME", "WHITESPACE", "COMMENT", "END_PATCH", 
                      "AS_TEXT", "END_CONTENT", "CONTENT_TEXT" ]

    RULE_addBlockHeader = 0
    RULE_addBlock = 1
    RULE_addBlockText = 2
    RULE_removeBlock = 3
    RULE_replaceNthBlockHeader = 4
    RULE_replaceNthBlock = 5
    RULE_replaceAllBlockHeader = 6
    RULE_replaceAllBlock = 7
    RULE_replaceBlockText = 8
    RULE_root = 9
    RULE_locationToken = 10

    ruleNames =  [ "addBlockHeader", "addBlock", "addBlockText", "removeBlock", 
                   "replaceNthBlockHeader", "replaceNthBlock", "replaceAllBlockHeader", 
                   "replaceAllBlock", "replaceBlockText", "root", "locationToken" ]

    EOF = Token.EOF
    ADD=1
    REMOVE=2
    REPLACE=3
    REPLACE_ALL=4
    FILENAME=5
    BEGIN_PATCH=6
    BEGIN_CONTENT=7
    FUNCTION=8
    END=9
    OPEN_BLOCK=10
    CLOSE_BLOCK=11
    INTEGER=12
    DASH=13
    FUNCTION_NAME=14
    WHITESPACE=15
    COMMENT=16
    END_PATCH=17
    AS_TEXT=18
    END_CONTENT=19
    CONTENT_TEXT=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class AddBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(PatchfileParser.ADD, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockHeader" ):
                listener.enterAddBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockHeader" ):
                listener.exitAddBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockHeader" ):
                return visitor.visitAddBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def addBlockHeader(self):

        localctx = PatchfileParser.AddBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_addBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(PatchfileParser.ADD)
            self.state = 23
            self.match(PatchfileParser.FILENAME)
            self.state = 24
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def addBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlock" ):
                listener.enterAddBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlock" ):
                listener.exitAddBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlock" ):
                return visitor.visitAddBlock(self)
            else:
                return visitor.visitChildren(self)




    def addBlock(self):

        localctx = PatchfileParser.AddBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_addBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.addBlockHeader()
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 31
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 32
            self.addBlockText()
            self.state = 33
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AS_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.AS_TEXT)
            else:
                return self.getToken(PatchfileParser.AS_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockText" ):
                listener.enterAddBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockText" ):
                listener.exitAddBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockText" ):
                return visitor.visitAddBlockText(self)
            else:
                return visitor.visitChildren(self)




    def addBlockText(self):

        localctx = PatchfileParser.AddBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_addBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 35
                self.match(PatchfileParser.AS_TEXT)
                self.state = 38 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==18):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RemoveBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REMOVE(self):
            return self.getToken(PatchfileParser.REMOVE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.LocationTokenContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,i)


        def DASH(self):
            return self.getToken(PatchfileParser.DASH, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_removeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemoveBlock" ):
                listener.enterRemoveBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemoveBlock" ):
                listener.exitRemoveBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRemoveBlock" ):
                return visitor.visitRemoveBlock(self)
            else:
                return visitor.visitChildren(self)




    def removeBlock(self):

        localctx = PatchfileParser.RemoveBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_removeBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(PatchfileParser.REMOVE)
            self.state = 41
            self.match(PatchfileParser.FILENAME)
            self.state = 42
            self.locationToken()
            self.state = 43
            self.match(PatchfileParser.DASH)
            self.state = 44
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE(self):
            return self.getToken(PatchfileParser.REPLACE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlockHeader" ):
                listener.enterReplaceNthBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlockHeader" ):
                listener.exitReplaceNthBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlockHeader" ):
                return visitor.visitReplaceNthBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlockHeader(self):

        localctx = PatchfileParser.ReplaceNthBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_replaceNthBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(PatchfileParser.REPLACE)
            self.state = 47
            self.match(PatchfileParser.FILENAME)
            self.state = 48
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def replaceNthBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlock" ):
                listener.enterReplaceNthBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlock" ):
                listener.exitReplaceNthBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlock" ):
                return visitor.visitReplaceNthBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlock(self):

        localctx = PatchfileParser.ReplaceNthBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_replaceNthBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 50
                self.replaceNthBlockHeader()
                self.state = 53 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==3):
                    break

            self.state = 55
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 56
            self.replaceBlockText()
            self.state = 57
            self.match(PatchfileParser.END_CONTENT)
            self.state = 58
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 59
            self.addBlockText()
            self.state = 60
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceAllBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE_ALL(self):
            return self.getToken(PatchfileParser.REPLACE_ALL, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceAllBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceAllBlockHeader" ):
                listener.enterReplaceAllBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceAllBlockHeader" ):
                listener.exitReplaceAllBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceAllBlockHeader" ):
                return visitor.visitReplaceAllBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def replaceAllBlockHeader(self):

        localctx = PatchfileParser.ReplaceAllBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_replaceAllBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(PatchfileParser.REPLACE_ALL)
            self.state = 63
            self.match(PatchfileParser.FILENAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceAllBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def replaceAllBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceAllBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceAllBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceAllBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceAllBlock" ):
                listener.enterReplaceAllBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceAllBlock" ):
                listener.exitReplaceAllBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceAllBlock" ):
                return visitor.visitReplaceAllBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceAllBlock(self):

        localctx = PatchfileParser.ReplaceAllBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_replaceAllBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 65
                self.replaceAllBlockHeader()
                self.state = 68 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==4):
                    break

            self.state = 70
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 71
            self.replaceBlockText()
            self.state = 72
            self.match(PatchfileParser.END_CONTENT)
            self.state = 73
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 74
            self.addBlockText()
            self.state = 75
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTENT_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.CONTENT_TEXT)
            else:
                return self.getToken(PatchfileParser.CONTENT_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceBlockText" ):
                listener.enterReplaceBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceBlockText" ):
                listener.exitReplaceBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceBlockText" ):
                return visitor.visitReplaceBlockText(self)
            else:
                return visitor.visitChildren(self)




    def replaceBlockText(self):

        localctx = PatchfileParser.ReplaceBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_replaceBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 77
                self.match(PatchfileParser.CONTENT_TEXT)
                self.state = 80 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==20):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockContext,i)


        def removeBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.RemoveBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.RemoveBlockContext,i)


        def replaceNthBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockContext,i)


        def replaceAllBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceAllBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceAllBlockContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = PatchfileParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0):
                self.state = 86
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 82
                    self.addBlock()
                    pass
                elif token in [2]:
                    self.state = 83
                    self.removeBlock()
                    pass
                elif token in [3]:
                    self.state = 84
                    self.replaceNthBlock()
                    pass
                elif token in [4]:
                    self.state = 85
                    self.replaceAllBlock()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 90
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocationTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PatchfileParser.RULE_locationToken

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FUNCTION(self):
            return self.getToken(PatchfileParser.FUNCTION, 0)
        def FUNCTION_NAME(self):
            return self.getToken(PatchfileParser.FUNCTION_NAME, 0)
        def OPEN_BLOCK(self):
            return self.getToken(PatchfileParser.OPEN_BLOCK, 0)
        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)
        def CLOSE_BLOCK(self):
            return self.getToken(PatchfileParser.CLOSE_BLOCK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)


    class EndContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END(self):
            return self.getToken(PatchfileParser.END, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd" ):
                return visitor.visitEnd(self)
            else:
                return visitor.visitChildren(self)


    class LineNumberContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLineNumber" ):
                return visitor.visitLineNumber(self)
            else:
                return visitor.visitChildren(self)



    def locationToken(self):

        localctx = PatchfileParser.LocationTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_locationToken)
        self._la = 0 # Token type
        try:
            self.state = 104
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8, 10]:
                localctx = PatchfileParser.FunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==10:
                    self.state = 91
                    self.match(PatchfileParser.OPEN_BLOCK)


                self.state = 94
                self.match(PatchfileParser.FUNCTION)
                self.state = 95
                self.match(PatchfileParser.FUNCTION_NAME)
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 96
                    self.match(PatchfileParser.INTEGER)


                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==11:
                    self.state = 99
                    self.match(PatchfileParser.CLOSE_BLOCK)


                pass
            elif token in [12]:
                localctx = PatchfileParser.LineNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.match(PatchfileParser.INTEGER)
                pass
            elif token in [9]:
                localctx = PatchfileParser.EndContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 103
                self.match(PatchfileParser.END)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





