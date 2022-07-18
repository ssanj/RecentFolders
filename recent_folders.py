import sublime
import sublime_plugin
from typing import List
import os
import json
import subprocess

class RecentFoldersCommand(sublime_plugin.WindowCommand):

  sublime_session_file = "Auto Save Session.sublime_session"
  fallback_sublime_session_file = "Session.sublime_session"

  sublime_exec = '/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl'

  def run(self):
    window = self.window

    if window:
      packages_dir: str = sublime.packages_path()
      sublime_dir: str = os.path.dirname(packages_dir)
      local_dir = f"{sublime_dir}/Local"
      session_file = f"{local_dir}/{RecentFoldersCommand.sublime_session_file}"
      fallback_session_file = f"{local_dir}/{RecentFoldersCommand.fallback_sublime_session_file}"
      session_exists = os.path.exists(session_file)
      fallback_exists = os.path.exists(fallback_session_file)
      session_file = session_file if session_exists else fallback_session_file

      if session_exists or fallback_exists:
        with open(session_file, 'r') as f:
          json_content = json.load(f)
          folder_history = json_content.get('folder_history')
          if folder_history:
            window.show_quick_panel(
              items = folder_history,
              placeholder = "Open Folder:",
              on_select = lambda index: self.on_select(self.window, folder_history, index),
            )
          else:
            self.show_error(f"could not find 'folder_history' key in Auto Save Session.sublime_session")
      else:
        self.show_error(f"{session_file} and {fallback_session_file} does not exist")
    else:
      sublime.message_dialog("No active window found")


  def on_select(self, window: sublime.Window, folder_history: List[str] ,index: int) -> None:
    if index >= 0 and len(folder_history) > index:
      subprocess.Popen([RecentFoldersCommand.sublime_exec, '-n', folder_history[index]])


  def show_error(self, message: str) -> None:
    sublime.message_dialog(message)
