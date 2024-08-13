from colorama import Fore,Style
class CMD():
    def __init__(self,prompt:str = "CMD>",intro:str = "Welcome in CMD!"):
        self.prompt = prompt
        self.intro = intro
        self.commands = dict()
        self.add_func_to_reg("help",self.helping,"Function what show you describe of other commands",True,1,1)
    def helping(self,what,razy:int = 1):
        if self.commands.get(what+"-d"):
            for x in range(razy):
                print(x,self.commands.get(what+"-d"))
        else:
            print(Fore.RED + "This command dosen't exist!",end="")
            print(Style.RESET_ALL)
    def add_func_to_reg(self,cmd:str,func,desc:str,arg:bool = False,amtr:int = 0,amtu:int = 0):
        if arg == True:
            self.commands.update({cmd:func,cmd+"-a":arg,cmd+"-aar":amtr,cmd+"-d":desc,cmd+"-aau":amtu})
        else:
            self.commands.update({cmd:func,cmd+"-a":arg,cmd+"-d":desc,})
    def prase(self,line:str):
        if  not line:
            print(Fore.RED + "You have to give command if you want me to give you reply. :)",end="")
            print(Style.RESET_ALL)
        else:
            if "|" in line:
                global cmds
                cmds = line.split("|")
                # print(cmds)
                for cmd in cmds:
                    command = cmd.split()
                    basecmd = command[0]
                    args = command
                    del command[0]
                    if basecmd in self.commands.keys():
                        if self.commands[basecmd+"-a"]:
                            amountarg = range(self.commands.get(basecmd+"-aar"),self.commands.get(basecmd+"-aar")+self.commands.get(basecmd+"-aau")+1)
                            amountargmin = self.commands.get(basecmd+"-aar")
                            amountargmax = self.commands.get(basecmd+"-aar")+self.commands.get(basecmd+"-aau")
                            try:
                                for x in amountarg:
                                    if x == len(args):
                                        pass
                                    elif len(args) < amountargmin:
                                        raise Exception("The number of arguments is insufficient")
                                    elif len(args) > amountargmax:
                                        raise Exception("You have given too many arguments.")
                            except Exception() as e:
                                print(Fore.RED + str(e),end="")
                                print(Style.RESET_ALL)
                            else:
                                    basearg = str()
                                    for x in args:
                                        basearg = basearg+x+','
                                        basearg = basearg[:-1]
                                        self.commands[basecmd](basearg)
                        else:
                            self.commands[basecmd]()
                    else:
                        print(Fore.RED + "This command dosen't exist!",end="")
                        print(Style.RESET_ALL)
            else:
                command = line.split()
                if len(command) == 0:
                    command = line
                basecmd = command[0]
                args = command
                del command[0]
                if basecmd in self.commands.keys():
                    if self.commands[basecmd+"-a"]:
                        amountarg = range(self.commands.get(basecmd+"-aar"),self.commands.get(basecmd+"-aar")+self.commands.get(basecmd+"-aau")+1)
                        amountargmin = self.commands.get(basecmd+"-aar")
                        amountargmax = self.commands.get(basecmd+"-aar")+self.commands.get(basecmd+"-aau")
                        try:
                            for x in amountarg:
                                if x == len(args):
                                    pass
                                elif len(args) < amountargmin:
                                    raise Exception("The number of arguments is insufficient")
                                elif len(args) > amountargmax:
                                    raise Exception("You have given too many arguments.")
                        except Exception as e:
                            print(Fore.RED + str(e),end="")
                            print(Style.RESET_ALL)
                        else:
                            basearg = str()
                            for x in args:
                                basearg = basearg+x+','
                                basearg = basearg[:-1]
                                self.commands[basecmd](basearg)
                    else:
                        return self.commands[basecmd]()
                else:
                    print(Fore.RED + "This command dosen't exist!",end="")
                    print(Style.RESET_ALL)
    def main_loop(self):
        global line
        print(self.intro)
        line = "start"
        while line != "exit":
            line = input(self.prompt)
            self.prase(line)
CMD().main_loop()