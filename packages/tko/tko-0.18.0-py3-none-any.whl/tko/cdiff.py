import curses
from .play.fmt import Fmt
from .run.basic import ExecutionResult
from .run.unit import Unit
from .run.param import Param
from .execution import Execution
from .run.diff import Diff
from .util.sentence import Sentence, Token, RToken
from typing import List, Tuple, Optional
from .play.frame import Frame
from .play.floating import Floating
from .play.floating_manager import FloatingManager
from .play.images import images, compilling, success, select
from .util.runner import Runner
from .util.freerun import Free
from .play.style import Style
from .game.task import Task
import random


from .run.wdir import Wdir
from .run.report import Report
from .settings.settings_parser import SettingsParser
import os
from .run.basic import Success
import enum

class Mode(enum.Enum):
    select = 0
    running = 1
    finished = 2

class Keys:
    left = "a"
    left2 = "h"
    up = "w"
    up2 = "k"
    right = "d"
    right2 = "l"
    down = "s"
    down2 = "k"
    principal = "p"
    diff = "m"
    executar = "e"
    testar = "t"
    sair = "q"

class CDiff:
    def __init__(self, wdir: Wdir, param: Param.Basic, success_type: Success):
        self.param = param
        self.results_done: List[Tuple[Token, int]] = []
        self.results_fail: List[Tuple[Token, int]] = []
        self.wdir = wdir
        self.unit_list = [unit for unit in wdir.get_unit_list()] # unit list to be consumed
        self.exit = False
        self.success_type = success_type
        self.task = Task()
        self.init = 0   # index of first line to show
        self.length = 1  # length of diff
        self.space = 0  # dy space for draw
        self.mode: Mode = Mode.select

        self.index = 0
        self.finished = False
        self.resumes: List[str] = []

        self.sp = SettingsParser()
        self.settings = self.sp.load_settings()
        self.colors = self.settings.geral.is_colored()
        self.first_loop = True
        self.fman = FloatingManager()
        self.first_run = False

    def set_first_run(self):
        self.first_run = True
        return self

    def save_settings(self):
        self.settings.geral.set_is_diff_down(self.param.is_up_down)
        self.sp.save_settings()
        return self
    
    def set_task(self, task: Task):
        self.task = task
        return self

    def set_exit(self):
        self.exit = True
        return self

    def end_processing(self):
        return (len(self.unit_list) == 0) or self.wdir.get_solver().compile_error

    def get_color(self, unit: Unit):
        if unit.result == ExecutionResult.SUCCESS:
            return "G"
        if unit.result == ExecutionResult.WRONG_OUTPUT:
            return "R"
        if unit.result == ExecutionResult.EXECUTION_ERROR:
            return "Y"
        if unit.result == ExecutionResult.COMPILATION_ERROR:
            return "Y"
        return ""

    def print_centered_image(self, image: str, color: str):
        _, cols = Fmt.get_size()
        lines = image.split("\n")[1:]
        for i, line in enumerate(lines):
            Fmt.write(i + 4, 1, Sentence().addf(color, line).center(cols - 2, Token(" ", " ")))

    def random_get(self, dic: dict, mode:str):
        if mode == "static":
            count = sum([ord(c) for c in self.get_folder()])
            keys = list(dic.keys())
            return dic[keys[count % len(keys)]]
        else:
            keys = list(dic.keys())
            return dic[random.choice(keys)]    

    def show_success(self):
        if self.success_type == Success.RANDOM:
            out = self.random_get(images, "static")
        else:
            out = self.random_get(success, "static")
        self.print_centered_image(out, "" if not self.colors else "g")
        
    def show_compilling(self):
        out = self.random_get(compilling, "random")
        self.print_centered_image(out, "" if not self.colors else "y")

    def draw_scrollbar(self):
        y_init = 3
        if len(self.results_fail) == 0:
            return   
        tr = "╮"
        br = "╯"
        vbar = "│"
        bar = []

        if self.length > self.space:
            total = self.space
            _begin = False
            _end = False
            if self.init == 0:
                _begin = True
            if self.init == self.length - self.space:
                _end = True

            pre = int((self.init / self.length) * total)
            mid = int((self.space / self.length) * total)
            pos = (max(0, total - pre - mid))

            if _begin:
                pre -= 1
            if _end:
                pos -= 1

            if self.init > 0 and pre == 0:
                pre = 1
                pos -= 1

            if _begin:
                bar.append(tr)
            for _ in range(pre):
                bar.append(vbar)
            for _ in range(mid):
                bar.append("┃")
            for _ in range(pos):
                bar.append(vbar)
            if _end:
                bar.append(br)

        elif self.length < self.space:
            bar.append(tr)
            for i in range(self.length - 2):
                bar.append(vbar)
            bar.append(br)

        _, cols = Fmt.get_size()
        for i in range(len(bar)):
            Fmt.write(i + y_init, cols - 1, Sentence().add(bar[i]))

    def get_folder(self):
        source_list = self.wdir.get_source_list()
        if source_list:
            folder = os.path.abspath(source_list[0])
        else:
            folder = os.path.abspath(self.wdir.get_solver().path_list[0])
        return folder.split(os.sep)[-2]

    def get_focused_unit(self) -> Optional[Unit]:
        if len(self.results_fail + self.results_done) == 0:
            return None
        join_list = self.results_fail + self.results_done
        _, index = join_list[self.index]
        unit = self.wdir.get_unit(index)
        return unit

    def process_one(self):
        solver = self.wdir.get_solver()
        if len(self.results_fail) != 0 and solver.compile_error:
            self.mode = Mode.running
            return
        if self.mode != Mode.running:
            return
        if len(self.unit_list) > 0:
            index = len(self.results_done) + len(self.results_fail)
            unit = self.unit_list[0]
            self.unit_list = self.unit_list[1:]
            unit.result = Execution.run_unit(solver, unit)
            symbol = ExecutionResult.get_symbol(unit.result)
            color = self.get_color(unit)
            if unit.result != ExecutionResult.SUCCESS:
                self.results_fail.append((Token(symbol.text, color), index))
            else:
                self.results_done.append((Token(symbol.text, color), index))
            self.task.test_progress = (len(self.results_done) * 100) // len(self.wdir.get_unit_list())
        else:
            self.mode = Mode.finished

    def draw_top_line(self):
        # construir mais uma solução
        activity_color = "W" if not self.colors else "C"
        solver_color = "M" if not self.colors else "M"
        sources_color = "W" if not self.colors else "Y"
        running_color = "W" if not self.colors else "R"

        _, cols = Fmt.get_size()
        frame = Frame(0, 0).set_size(3, cols)
        folder = self.get_folder()
        activity = Sentence().addf(activity_color, folder)
        solvers = Sentence()
        for i, solver in enumerate(self.get_solver_names()):
            # if i != 0:
            #     solvers.addf(solver_color, ", ")
            color = solver_color
            if i == self.task.main_index:
                color = "G"
            solvers.addf(color.lower(), Style.roundL()).addf(color, solver).addf(color.lower(), Style.roundR())

        sources = Sentence()
        for i, (source, _) in enumerate(self.wdir.sources_names()):
            if i != 0:
                sources.add(", ")
            sources.addf(sources_color, source)

        done = len(self.results_done) + len(self.results_fail)
        full = len(self.wdir.get_unit_list())
        sources.addf(sources_color, f"({full})")
        # solvers = Sentence().addf(solver_color.lower(), Style.roundL()).add(solvers).addf(solver_color.lower(), Style.roundR())
        activity = Sentence().addf(activity_color.lower(), Style.roundL()).add(activity).addf(activity_color.lower(), Style.roundR())
        if done != full:
            activity.addf(running_color.lower(), Style.roundL()).addf(running_color, f"({done}/{full})").addf(running_color.lower(), Style.roundR())
        sources = Sentence().addf(sources_color.lower(), Style.roundL()).add(sources).addf(sources_color.lower(), Style.roundR())

        delta = frame.get_dx() - solvers.len()
        left = 1
        right = 1
        if delta > 0:
            delta_left = delta // 2
            left = max(1, delta_left - activity.len())
            delta_right = delta - delta_left
            right = max(1, delta_right - sources.len())

        header = Sentence().add(activity).add("─" * left).add(solvers).add("─" * right).add(sources)

        frame.set_header(header)


        value = self.get_focused_unit()
        if value is not None:
            frame.write(0, 0, Sentence().add(value.str(False)).center(frame.get_dx()))


        i = 0
        output = Sentence()
        for symbol, index in self.results_fail + self.results_done:
            foco = i == self.index
            extrap = Token(Style.roundL(), symbol.fmt.lower()) if not foco else Token(Style.roundL(), "")
            extras = Token(Style.roundR(), symbol.fmt.lower()) if not foco else Token(Style.roundR(), "")
            output.add(extrap).addf(symbol.fmt, str(index).zfill(2)).add(symbol).add(extras).add(" ")
            i += 1

        size = 8
        if self.index * 8 > frame.get_dx():
            output.cut_begin((self.index + 1) * 8 - frame.get_dx())

        frame.set_footer(output, "")
        frame.draw()
        
    def draw_bottom_line(self):
        tokens = [
            RToken("G", "Sair[q]"),
            RToken("Y", "Executar[e]"),
            RToken("Y", "Testar[t]"),
            RToken("C", "Principal[p]"),
            RToken("C", "Navegar[wasd]"),
        ]
        if self.settings.geral.is_diff_down():
            tokens.append(RToken("G", "cima╾lado[m]")) 
        else:
            tokens.append(RToken("G", "cima╼lado[m]"))

        cmds = Sentence()
        for t in tokens:
            color = "W" if not self.colors else t.fmt
            cmds.addf(color.lower(), Style.roundL()).addf(color, t.text).addf(color.lower(), Style.roundR()).add(" ")
        lines, cols = Fmt.get_size()
        Fmt.write(lines - 1, 0, cmds.center(cols, Token(" ")))
 
    def draw_main(self, unit: Unit):
        lines, cols = Fmt.get_size()
        self.space = lines - 4
        frame = Frame(2, -1).set_inner(self.space, cols - 1).set_border_square()

        if len(self.results_fail) == 0 and self.end_processing():
            self.show_success()
            return
        Report.set_terminal_size(cols)
        
        if self.wdir.get_solver().compile_error:
            received = self.wdir.get_solver().error_msg
            line_list = [Sentence().add(line) for line in received.split("\n")]
        elif self.param.is_up_down:
            line_list = Diff.mount_up_down_diff(unit, curses=True)
        else:
            line_list = Diff.mount_side_by_side_diff(unit, curses=True)

        self.length = max(1, len(line_list))

        if self.length - self.init < self.space:
            self.init = max(0, self.length - self.space)

        if self.init >= self.length:
            self.init = self.length - 1

        if self.init < self.length:
            line_list = line_list[self.init:]
        for i, line in enumerate(line_list):
            frame.write(i, 0, Sentence().add(line))
        return

    def load_autoload_warning(self):
        if not self.wdir.is_autoload():
            return
        warning = Floating().set_header(" Seja bem vindo ").warning()
        warning.put_text("")
        warning.put_sentence(Sentence().addf("r", "Todos") + " os arquivos de código da pasta foram carregados automaticamente")
        warning.put_text("Sempre verifique no topo da tela quais arquivos foram carregados.")
        warning.put_text("Remova ou renomeie da pasta alvo os arquivo que não quer utilizar.")
        warning.put_text("")
        warning.put_text("Você também pode escolher quais arquivos deseja executar")
        warning.put_text("navegando até a pasta de destino e executando")
        warning.put_text("o comando 'tko run' com os arquivos desejados")
        warning.put_text("")
        warning.put_sentence(Sentence().addf("c", "tko run <arquivos> cases.tio")) 
        warning.put_text("")
        warning.put_sentence(Sentence().addf("r", "Exemplo: ").addf("c", "tko run main.c lib.c cases.tio")) 
        warning.put_text("")

        self.fman.add_input(warning)

    def get_solver_names(self):
        return sorted(self.wdir.solvers_names())
    
    def main(self, scr):
        self.mode = Mode.select
        curses.curs_set(0)  # Esconde o cursor
        Fmt.init_colors()  # Inicializa as cores
        Fmt.set_scr(scr)  # Define o scr como global
        while not self.exit:
            if self.first_loop and self.first_run:
                self.first_loop = False
                self.load_autoload_warning()
            Fmt.erase()
            if self.mode == Mode.running:
                if self.wdir.get_solver().not_compiled():
                    self.show_compilling()
                    Fmt.refresh()
                    Fmt.erase()
                    self.wdir.get_solver().prepare_exec()
                self.process_one()
            self.draw_top_line()
            unit = self.get_focused_unit()
            if unit is not None:
                self.draw_main(unit)
                if not self.wdir.get_solver().compile_error:
                    self.draw_scrollbar()
            else:
                self.print_centered_image(select, "y")
            
            self.draw_bottom_line()

            if self.fman.has_floating():
                self.fman.draw_warnings()

            if self.mode == Mode.running and not self.end_processing():
                Fmt.refresh()
                continue

            if self.fman.has_floating():
                key = self.fman.get_input()
            else:
                key = Fmt.getch()

            fn_exec = self.process_key(key)
            if fn_exec is not None:
                return fn_exec

    def run_exec_mode(self):
        self.mode = Mode.running
        if self.wdir.is_autoload():
            self.wdir.autoload()
            self.wdir.get_solver().set_main(self.get_solver_names()[self.task.main_index])
        return lambda: Free.free_run(self.wdir.get_solver(), show_compilling=True, to_clear=True, wait_input=True)

    def run_test_mode(self):
        self.mode = Mode.running
        self.index = 0
        if self.wdir.is_autoload():
            self.wdir.autoload()
        Fmt.erase()
        self.show_compilling()
        Fmt.refresh()
        self.wdir.get_solver().set_main(self.get_solver_names()[self.task.main_index]).prepare_exec()
        self.results_done = []
        self.results_fail = []
        self.unit_list = [unit for unit in self.wdir.get_unit_list()]

    def send_char_not_found(self, key):
        self.fman.add_input(Floating("v>").error()
                    .put_text("Tecla")
                    .put_text(f"char {chr(key)}")
                    .put_text(f"code {key}")
                    .put_text("não reconhecida")
                    .put_text("")
                    )

    def go_left(self):
        self.index = max(0, self.index - 1)
        self.init = 0

    def go_right(self):
        self.index = min(len(self.results_done) + len(self.results_fail) - 1, self.index + 1)
        self.init = 0

    def go_down(self):
        self.init += 1

    def go_up(self):
        self.init = max(0, self.init - 1)

    def process_key(self, key):
        if key == ord('q'):
            self.set_exit()
        elif key == curses.KEY_LEFT or key == ord(Keys.left) or key == ord(Keys.left2):
            self.go_left()
        elif key == curses.KEY_RIGHT or key == ord(Keys.right) or key == ord(Keys.right2):
            self.go_right()
        elif key == curses.KEY_DOWN or key == ord(Keys.down) or key == ord(Keys.down2):
            self.go_down()
        elif key == curses.KEY_UP or key == ord(Keys.up) or key == ord(Keys.up2):
            self.go_up()
        elif key == ord(Keys.diff):
            self.param.is_up_down = not self.param.is_up_down
            self.save_settings()
            self.init = 0
        elif key == ord(Keys.principal):
            self.task.main_index = (self.task.main_index + 1) % len(self.get_solver_names())
        elif key == ord(Keys.executar):
            return self.run_exec_mode()
        elif key == ord(Keys.testar):
            self.run_test_mode()
        elif key != -1:
            self.send_char_not_found(key)

    def run(self):
        while True:
            free_run_fn = curses.wrapper(self.main)
            if free_run_fn == None:
                break
            else:
                while(free_run_fn()):
                    pass
