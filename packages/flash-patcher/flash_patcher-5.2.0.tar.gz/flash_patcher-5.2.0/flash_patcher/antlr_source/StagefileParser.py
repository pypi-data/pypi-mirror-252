# Generated from ../flash_patcher/antlr_source/Stagefile.g4 by ANTLR 4.13.1
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
        4,1,5,23,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,1,1,1,2,1,2,
        1,3,1,3,1,3,5,3,18,8,3,10,3,12,3,21,9,3,1,3,0,0,4,0,2,4,6,0,0,21,
        0,8,1,0,0,0,2,10,1,0,0,0,4,12,1,0,0,0,6,19,1,0,0,0,8,9,5,1,0,0,9,
        1,1,0,0,0,10,11,5,2,0,0,11,3,1,0,0,0,12,13,5,3,0,0,13,5,1,0,0,0,
        14,18,3,0,0,0,15,18,3,2,1,0,16,18,3,4,2,0,17,14,1,0,0,0,17,15,1,
        0,0,0,17,16,1,0,0,0,18,21,1,0,0,0,19,17,1,0,0,0,19,20,1,0,0,0,20,
        7,1,0,0,0,21,19,1,0,0,0,2,17,19
    ]

class StagefileParser ( Parser ):

    grammarFileName = "Stagefile.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "PATCH_FILE", "PYTHON_FILE", "ASSET_PACK_FILE", 
                      "WHITESPACE", "COMMENT" ]

    RULE_patchFile = 0
    RULE_pythonFile = 1
    RULE_assetPackFile = 2
    RULE_root = 3

    ruleNames =  [ "patchFile", "pythonFile", "assetPackFile", "root" ]

    EOF = Token.EOF
    PATCH_FILE=1
    PYTHON_FILE=2
    ASSET_PACK_FILE=3
    WHITESPACE=4
    COMMENT=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PatchFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PATCH_FILE(self):
            return self.getToken(StagefileParser.PATCH_FILE, 0)

        def getRuleIndex(self):
            return StagefileParser.RULE_patchFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPatchFile" ):
                listener.enterPatchFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPatchFile" ):
                listener.exitPatchFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPatchFile" ):
                return visitor.visitPatchFile(self)
            else:
                return visitor.visitChildren(self)




    def patchFile(self):

        localctx = StagefileParser.PatchFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_patchFile)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.match(StagefileParser.PATCH_FILE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PythonFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_FILE(self):
            return self.getToken(StagefileParser.PYTHON_FILE, 0)

        def getRuleIndex(self):
            return StagefileParser.RULE_pythonFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPythonFile" ):
                listener.enterPythonFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPythonFile" ):
                listener.exitPythonFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPythonFile" ):
                return visitor.visitPythonFile(self)
            else:
                return visitor.visitChildren(self)




    def pythonFile(self):

        localctx = StagefileParser.PythonFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_pythonFile)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.match(StagefileParser.PYTHON_FILE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssetPackFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSET_PACK_FILE(self):
            return self.getToken(StagefileParser.ASSET_PACK_FILE, 0)

        def getRuleIndex(self):
            return StagefileParser.RULE_assetPackFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssetPackFile" ):
                listener.enterAssetPackFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssetPackFile" ):
                listener.exitAssetPackFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssetPackFile" ):
                return visitor.visitAssetPackFile(self)
            else:
                return visitor.visitChildren(self)




    def assetPackFile(self):

        localctx = StagefileParser.AssetPackFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assetPackFile)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(StagefileParser.ASSET_PACK_FILE)
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

        def patchFile(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StagefileParser.PatchFileContext)
            else:
                return self.getTypedRuleContext(StagefileParser.PatchFileContext,i)


        def pythonFile(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StagefileParser.PythonFileContext)
            else:
                return self.getTypedRuleContext(StagefileParser.PythonFileContext,i)


        def assetPackFile(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StagefileParser.AssetPackFileContext)
            else:
                return self.getTypedRuleContext(StagefileParser.AssetPackFileContext,i)


        def getRuleIndex(self):
            return StagefileParser.RULE_root

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

        localctx = StagefileParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 14) != 0):
                self.state = 17
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 14
                    self.patchFile()
                    pass
                elif token in [2]:
                    self.state = 15
                    self.pythonFile()
                    pass
                elif token in [3]:
                    self.state = 16
                    self.assetPackFile()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





