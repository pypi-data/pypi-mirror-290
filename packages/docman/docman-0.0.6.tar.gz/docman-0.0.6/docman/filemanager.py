import filecmp
import os
import sys
from argparse import ArgumentParser
from typing import List, Tuple, Optional

from .console import clear, black, blue, yellow, green, red, cyan, purple


class FileManager:

    def __init__(self, root_dir: str):
        self._root_dir = root_dir
        self._last_error = None
        self._list_entries: Optional[List[str]] = None
        self._menu_items = [
            (('MENU',), 'Menu', self.menu,
             ['MENU']),
            (('LIST','LS'), 'List Entries', self.list_entries,
             ['LIST [ENTRIES] [LIKE <pattern>]',
              'LIST [ENTRIES] AGAIN',
              'LIST LINKS [LIKE <pattern>]',
              'LIST LINKS AGAIN',
              'LIST DETAILS [LIKE <pattern>]',
              'LIST DETAILS AGAIN',
              'LIST REFERENCES TO <index>',
              'LIST REFS TO <index>',
              'LIST [ENTRIES] IN <index>',
             ]),
            (('VIEW',), 'View Entry', self.view_entry,
             ['VIEW <index>']),
            (('OPEN',), 'Open Entry', self.open_entry,
             ['OPEN <index>']),
            (('RENAME',), 'Rename Entry', self.rename_entry,
             ['RENAME <index> TO <new-name>', 'RENAME <index>']),
            (('GO', 'GOTO', 'CD'), 'Go to an Entry', self.go_to_entry,
             ['GO TO <index>',
              'GOTO <index>',
              'GO TO <entry>',
              'GO BACK',
              'GO HOME']),
            (('RETURN',), 'Return to prior Entry', self.go_back,
             ['RETURN']),
            (('DELETE',), 'Delete an Entry', self.delete_entry,
             ['DELETE <index>']),
            (('MERGE',), 'Merge two entries', self.merge_entry,
             ['MERGE <index-1> INTO <index-2>']),
            (('MOVE',), 'Move a file into a folder', self.move_entry,
             ['MOVE <index-1> INTO <index-2>']),
            (('CREATE',), 'Create entry', self.create_entry,
             ['CREATE FOLDER <name>']),
            (('FIND',), 'Find entries', self.find_entries,
             ['FIND <pattern>']),
            (('VERIFY',), 'Verify database', self.verify_database,
             ['VERIFY']),
            (('HELP',), 'Help', self.help,
             ['HELP <command>']),
            (('QUIT', 'EXIT'), 'Quit App', self.quit_app,
             ['QUIT',
              'EXIT']),
        ]
        self._database_dir = os.path.join(self._root_dir, 'Database')
        if not os.path.lexists(self._database_dir):
            print(f'{red}Missing folder {self._database_dir}')
            yesno = input(f'{yellow}Would you like to create the missing folder [N] ? {black}')
            if yesno.upper().startswith('Y'):
                os.makedirs(self._database_dir)
            if not os.path.lexists(self._database_dir):
                raise RuntimeError(f'Missing folder {self._database_dir}')
        self._dir_history = [self._database_dir]

    def _cur_dir(self):
        return self._dir_history[-1]

    def _push_dir_path(self, path: str):
        self._dir_history.append(path)
        self._list_entries = None

    def _pop_dir_path(self):
        while len(self._dir_history) > 1:
            self._dir_history.pop()
            self._list_entries = None
            if os.path.lexists(self._cur_dir()):
                return
        return

    def _pop_to_home(self):
        self._dir_history = [self._dir_history[0]]
        return

    def verify_database(self, request: List[str]):
        count_dirs = 0
        count_files = 0
        count_links = 0
        count_errors = 0
        for root_path, dir_names, file_names in os.walk(self._database_dir):
            entry_count, link_count, error_count = self._verify_entries(root_path, dir_names)
            count_dirs += entry_count
            count_links += link_count
            count_errors += error_count
            entry_count, link_count, error_count = self._verify_entries(root_path, file_names)
            count_files += entry_count
            count_links += link_count
            count_errors += error_count
        if count_errors > 0:
            print()
            print(f'{green}{count_dirs} Folders , {count_files} Files , {count_links} References, {red}{count_errors} Errors{black}')
        else:
            print(f'{green}{count_dirs} Folders , {count_files} Files , {count_links} References, {count_errors} Errors{black}')

    def _verify_entries(self, root_path, dir_names) -> Tuple[int, int, int]:
        count_entries = 0
        count_links = 0
        count_errors = 0
        for dir_name in dir_names:
            dir_path = os.path.join(root_path, dir_name)
            if os.path.islink(dir_path):
                count_links += 1
                real_path = os.path.realpath(dir_path)
                rel_path = self.rel_path(real_path)
                if not os.path.lexists(real_path):
                    print(f'{red}Missing target {rel_path}')
                    self._repair_missing_target(dir_path, real_path, root_path)
                    count_errors += 1
                elif not rel_path.startswith('Database/'):
                    print(f'{red}Reference to external resource {rel_path}')
                    count_errors += 1
            else:
                count_entries += 1
        return count_entries, count_links, count_errors

    def _repair_missing_target(self, dir_path, real_path, root_path):
        target_name = os.path.basename(real_path)
        for root, dirs, files in os.walk(self._database_dir):
            for dir in dirs:
                if dir == target_name:
                    new_dir_path = os.path.join(root, dir)
                    new_rel_path = self.rel_path(new_dir_path)
                    print()
                    print(f'{purple}{new_rel_path}{black}')
                    print()
                    yesno = input(f'{yellow}Would you like to link to here [N] ? {black}')
                    if yesno.upper().startswith('Y'):
                        link_target = os.path.relpath(new_dir_path, root_path)
                        os.remove(dir_path)
                        if os.path.lexists(dir_path):
                            raise ValueError(f'Failed to remove old "{self.rel_path(dir_path)}"')
                        os.symlink(link_target, dir_path)
                        if not os.path.lexists(dir_path):
                            raise ValueError(f'Failed to create "{self.rel_path(dir_path)}"')
                        return

    def create_entry(self, request: List[str]):
        if len(request) > 0:
            if request[0].upper() == 'FOLDER':
                new_name = ' '.join(request[1:])
                entry_path = os.path.join(self._cur_dir(), new_name)
                if os.path.lexists(entry_path):
                    raise ValueError(f'Entry already exists here named "{new_name}"')
                database_path = os.path.join(self._database_dir, new_name)
                if not os.path.lexists(database_path):
                    os.mkdir(database_path)
                else:
                    print()
                    print(f'{purple}Existing folder "{new_name}"{black}')
                    print()
                    yesno = input(f'{yellow}Do you want to link to the existing folder [N] ? {black}')
                    if not yesno.upper().startswith('Y'):
                        return
                if not os.path.lexists(entry_path):
                    link_target = os.path.relpath(database_path, self._cur_dir())
                    os.symlink(link_target, entry_path)
                    if not os.path.lexists(entry_path):
                        raise ValueError(f'Failed to create "{new_name}"')
                return
        self.help(['CREATE'])

    def _parse_entry_criteria(self, request: List[str]):
        show_links = False
        show_references = False
        show_details = False
        if len(request) > 0:
            if request[0].upper() == 'ENTRIES':
                request.pop(0)
            if request[0].upper() == 'DETAILS':
                show_details = True
                request.pop(0)
            elif request[0].upper() == 'LINKS':
                show_links = True
                request.pop(0)
            elif request[0].upper() in ('REFS', 'REFERENCES'):
                show_references = True
                request.pop(0)
        return show_links, show_references, show_details

    def find_entries(self, request: List[str]):
        show_links, show_references, show_details = self._parse_entry_criteria(request)
        likes = request
        entries = []
        for root, dirs, files in os.walk(self._database_dir, followlinks=False):
            for dir in dirs:
                if self._is_like(dir, likes):
                    act_path = os.path.join(root, dir)
                    entries.append(act_path)
            for file in files:
                if self._is_like(file, likes):
                    act_path = os.path.join(root, file)
                    entries.append(act_path)
        self._list_entries = sorted(entries)
        self._list_current_entries(show_details=show_details, show_links=show_links)

    def list_entries(self, request: List[str]):
        show_links, show_references, show_details = self._parse_entry_criteria(request)
        if len(request) > 1:
            if show_references:
                if request[0].upper() == 'TO':
                    entry, index, entry_path = self._lookup_index_entry(request[1])
                    self._list_references_to_entry(entry_path)
                    return
                raise ValueError(f'Expected LIST REFERENCES TO <index>')
            if request[0].upper() == 'IN':
                entry, index, entry_path = self._lookup_index_entry(request[1])
                self._list_entries_in_entry(entry_path, show_details=show_details, show_links=show_links)
                return
        if len(request) > 0:
            if request[0].upper() == 'AGAIN':
                self._list_current_entries(show_details=show_details, show_links=show_links)
                return
        likes = request[1:] if len(request) > 1 and request[0].upper() == 'LIKE' else []
        entries = [
            os.path.join(self._cur_dir(), entry)
            for entry in os.listdir(self._cur_dir())
            if self._is_like(entry, likes)
        ]
        self._list_entries = sorted(entries)
        self._list_current_entries(show_details=show_details, show_links=show_links)

    def _is_like(self, entry: str, likes: List[str]):
        words = [word.lower() for word in entry.split()]
        likes = [like.lower() for like in likes]
        for like in list(likes):
            if like.startswith('*') and like.endswith('*'):
                matched = False
                for word in words:
                    if like[1:-1] in word:
                        matched = True
                        words.remove(word)
                        break
                if not matched:
                    return False
                continue
            if like.endswith('*'):
                matched = False
                for word in words:
                    if word.startswith(like[0:-1]):
                        matched = True
                        words.remove(word)
                        break
                if not matched:
                    return False
                continue
            if like.startswith('*'):
                matched = False
                for word in words:
                    if word.endswith(like[1:]):
                        matched = True
                        words.remove(word)
                        break
                if not matched:
                    return False
                continue
            if like in words:
                words.remove(like)
                continue
            else:
                return False
        return True

    def _list_references_to_entry(self, entry_path):
        references = self._find_references(entry_path)
        for index, reference in enumerate(references):
            if os.path.isdir(reference):
                print(f'{blue}{index + 1:3} - {self.rel_path(reference)}{black}')
            elif os.path.isfile(reference):
                print(f'{purple}{index + 1:3} - {self.rel_path(reference)}{black}')
            else:
                print(f'{red}{index + 1:3} - {self.rel_path(reference)}{black}')

    def _list_current_entries(self, *, show_details=False, show_links=False):
        self._list_relative_entries(self._list_entries, show_details=show_details, show_links=show_links)

    def _list_relative_entries(self, entries, *, show_details=False, show_links=False):
        for index, entry_path in enumerate(entries):
            dir_path = os.path.dirname(entry_path)
            entry = os.path.basename(entry_path)

            if os.path.isdir(entry_path):
                entry_text = [f'{blue}{index+1:3} - {entry}']
            elif os.path.isfile(entry_path):
                entry_text = [f'{purple}{index + 1:3} - {entry}']
            else:
                entry_text = [f'{red}{index+1:3} - {entry}']

            if show_details:
                stat = os.stat(entry_path)
                entry_text.append(f'{cyan}(Size: {stat.st_size:,})')

            if os.path.islink(entry_path):
                link_target = self.rel_path(os.path.realpath(entry_path))
                if os.path.isdir(entry_path):
                    if show_links:
                        entry_text.append(f'{cyan}({link_target})')
                elif os.path.isfile(entry_path):
                    if show_links:
                        entry_text.append(f'{cyan}({link_target})')
                else:
                    if show_links:
                        entry_text.append(f'{cyan}({link_target})')

            if dir_path != self._cur_dir():
                rel_path = self.rel_path(dir_path)
                entry_text.append(f'{green}({rel_path})')

            print(*entry_text, f'{black}')

    def view_entry(self, request: List[str]):
        print(f'{red}Not implemented yet{black}')

    def open_entry(self, request: List[str]):
        for item in request:
            entry, index, entry_path = self._lookup_index_entry(item)
            if os.path.lexists(entry_path):
                if os.path.isfile(entry_path):
                    print(f'{green}Open {self.rel_path(entry_path)}{black}')
                    safe_path = entry_path.replace("'", "'\\''")
                    os.system(f'xdg-open \'{safe_path}\'')

    def delete_entry(self, request: List[str]):
        if len(request) == 1:
            entry, index, entry_path = self._lookup_index_entry(request[0])
            if not os.path.lexists(entry_path):
                raise ValueError(f'"{entry}" does not exist')
            if os.path.islink(entry_path):
                print(f'{purple}Deleting reference {self.rel_path(entry_path)}{black}')
                print()
                yesno = input(f'{yellow}Are you sure [N] ? {black}')
                if yesno.upper().startswith('Y'):
                    os.remove(entry_path)
                    del self._list_entries[index-1]
                    self._list_current_entries()
                return
            elif os.path.isfile(entry_path):
                print(f'{purple}Deleting file {self.rel_path(entry_path)}{black}')
                print()
                yesno = input(f'{yellow}Are you sure [N] ? {black}')
                print()
                if yesno.upper().startswith('Y'):
                    os.remove(entry_path)
                    del self._list_entries[index - 1]
                    self._list_current_entries()
                return
            raise ValueError(f'Do not currently support deleting folders')
        self.help(['DELETE'])

    def rename_entry(self, request: List[str]):
        if len(request) == 1:
            entry, index, entry_path = self._lookup_index_entry(request[0])
            print(f'{blue}{index} - {entry}{black}')
            print()
            entry_dir = os.path.dirname(entry_path)
            new_name = input(f'{yellow}Rename to ? {black}')
        elif len(request) >= 3:
            if request[1].upper() != 'TO':
                self.help(['RENAME'])
                return
            entry, index, entry_path = self._lookup_index_entry(request[0])
            entry_dir = os.path.dirname(entry_path)
            new_name = ' '.join(request[2:])
        else:
            self.help(['RENAME'])
            return
        print()
        print(f'{purple}Rename {entry}{black}')
        print(f'{purple}    To {new_name}{black}')
        print()
        yesno = input(f'{yellow}Are you sure [N] ? {black}')
        if yesno.upper().startswith('Y'):
            new_path = os.path.join(entry_dir, new_name)
            if os.path.lexists(new_path):
                raise ValueError(f'"{new_name}" already exists')
            if not os.path.lexists(entry_path):
                raise ValueError(f'"{entry}" does not exist')
            if os.path.islink(entry_path):
                self._rename_link(index, entry_path, new_path, new_name)
            else:
                self._rename_file_or_directory(index, entry_path, new_path, new_name)

    def move_entry(self, request: List[str]):
        if len(request) != 3:
            self.help(['MOVE'])
            return
        if request[1].upper() != 'INTO':
            self.help(['MOVE'])
            return
        from_entry, from_index, from_entry_path = self._lookup_index_entry(request[0])
        into_entry, into_index, into_entry_path = self._lookup_index_entry(request[2])
        print(f'{purple}Move {from_index} - {from_entry} {black}')
        print(f'{purple}Into {into_index} - {into_entry} {black}')
        print()
        yesno = input(f'{yellow}Are you sure [N] ? {black}')
        if yesno.upper().startswith('Y'):
            if not os.path.isfile(from_entry_path):
                raise ValueError(f'"{from_entry}" is not a file')
            if not os.path.isdir(into_entry_path):
                raise ValueError(f'"{from_entry}" is not a folder')
            target_path = os.path.join(into_entry_path, from_entry)
            if os.path.exists(target_path):
                raise ValueError(f'"{from_entry}" already exists in the folder')
            os.rename(from_entry_path, target_path)
            if not os.path.exists(target_path):
                raise ValueError(f'"{from_entry}" failed to move into the folder')
            if os.path.lexists(from_entry_path):
                raise ValueError(f'"{from_entry}" failed to move from this folder')
            del self._list_entries[from_index - 1]
            self._list_current_entries()

    def merge_entry(self, request: List[str]):
        if len(request) != 3:
            self.help(['MERGE'])
            return
        if request[1].upper() != 'INTO':
            self.help(['MERGE'])
            return
        from_entry, from_index, from_entry_path = self._lookup_index_entry(request[0])
        into_entry, into_index, into_entry_path = self._lookup_index_entry(request[2])
        print(f'{purple}Merge {from_index} - {from_entry} {black}')
        print(f'{purple} Into {into_index} - {into_entry} {black}')
        print()
        yesno = input(f'{yellow}Are you sure [N] ? {black}')
        if yesno.upper().startswith('Y'):
            if os.path.islink(from_entry_path) or os.path.islink(into_entry_path):
                self._merge_links(from_entry, from_index, from_entry_path, into_entry_path)
                return
            if os.path.isfile(from_entry_path) or os.path.isfile(into_entry_path):
                raise ValueError(f'Cannot merge files')
            self._merge_directory_contents(from_entry_path, into_entry_path)
            if self._relink_merged_from_entry(from_entry_path, into_entry_path):
                del self._list_entries[from_index - 1]
                self._list_current_entries()


    def _relink_merged_from_entry(self, from_entry_path, into_entry_path) -> bool:
        remainder = os.listdir(from_entry_path)
        if len(remainder) == 0:
            self._relink_references(from_entry_path, into_entry_path)
            os.rmdir(from_entry_path)
            if os.path.lexists(from_entry_path):
                raise ValueError(f'Could not remove "{self.rel_path(from_entry_path)}"')
            return True
        return False

    def _merge_directory_contents(self, from_entry_path, into_entry_path):
        if not os.path.isdir(from_entry_path) or not os.path.isdir(into_entry_path):
            raise ValueError(f'Can only merge folders')
        for entry in os.listdir(from_entry_path):
            from_path = os.path.join(from_entry_path, entry)
            into_path = os.path.join(into_entry_path, entry)
            if os.path.islink(from_path) or os.path.islink(into_path):
                self._merge_entry_link(entry, from_path, into_path)
                continue
            if os.path.isfile(from_path) or os.path.isfile(into_path):
                self._merge_entry_file(entry, from_path, into_path)
                continue
            if os.path.isdir(from_path) or os.path.isdir(into_path):
                raise ValueError(f'Do not support merging folders "{entry}"')

    def _merge_links(self, from_entry, from_index, from_entry_path, into_entry_path):
        if not os.path.islink(from_entry_path) or not os.path.islink(into_entry_path):
            raise ValueError(f'Cannot merge reference and non-reference')
        from_target_path = os.path.realpath(from_entry_path)
        into_target_path = os.path.realpath(into_entry_path)
        if from_target_path != into_target_path:
            if not self._merge_different_targets(from_target_path, into_target_path):
                return
        os.remove(from_entry_path)
        if os.path.lexists(from_entry_path):
            raise ValueError(f'Could not remove {from_entry}')
        del self._list_entries[from_index - 1]
        self._list_current_entries()

    def _merge_different_targets(self, from_target_path, into_target_path) -> bool:
        print()
        print(f'{cyan}Real Source is {self.rel_path(from_target_path)}{black}')
        print(f'{cyan}Real Target is {self.rel_path(into_target_path)}{black}')
        print()
        yesno = input(f'{yellow}Do you want to merge the real source into the real target [N] ? {black}')
        print()
        if yesno.upper().startswith('N'):
            return False
        self._merge_directory_contents(from_target_path, into_target_path)
        if self._relink_merged_from_entry(from_target_path, into_target_path):
            return True
        return False

    def _merge_entry_link(self, entry, from_path, into_path):
        if not os.path.lexists(into_path):
            os.rename(from_path, into_path)
            if not os.path.lexists(into_path):
                raise ValueError(f'Failed to merge "{self.rel_path(into_path)}"')
            return
        if not os.path.islink(from_path) or not os.path.islink(into_path):
            raise ValueError(f'Cannot merge reference and non reference "{entry}"')
        from_target = os.path.realpath(from_path)
        into_target = os.path.realpath(into_path)
        if from_target != into_target:
            raise ValueError(f'Cannot merge different references named "{entry}"')
        os.remove(from_path)
        if os.path.lexists(from_path):
            raise ValueError(f'Failed to remove "{self.rel_path(from_path)}"')

    def _merge_entry_file(self, entry, from_path, into_path):
        if not os.path.lexists(into_path):
            os.rename(from_path, into_path)
            if not os.path.lexists(into_path):
                raise ValueError(f'Failed to merge "{self.rel_path(into_path)}"')
            return
        if not os.path.isfile(from_path) or not os.path.isfile(into_path):
            raise ValueError(f'Cannot merge file and not file "{entry}"')
        if not filecmp.cmp(from_path, into_path, shallow=False):
            raise ValueError(f'Cannot merge files which are different "{entry}"')
        os.remove(from_path)
        if os.path.lexists(from_path):
            raise ValueError(f'Failed to remove "{self.rel_path(from_path)}"')

    def _find_references(self, entry_path: str) -> List[str]:
        real_path = os.path.realpath(entry_path)
        references: List[str] = []
        for root_path, dir_names, file_names in os.walk(self._database_dir):
            for file_name in file_names:
                file_path = os.path.join(root_path, file_name)
                if os.path.islink(file_path):
                    target = os.path.realpath(file_path)
                    if target == real_path:
                        references.append(file_path)
            for dir_name in dir_names:
                dir_path = os.path.join(root_path, dir_name)
                if os.path.islink(dir_path):
                    target = os.path.realpath(dir_path)
                    if target == real_path:
                        references.append(dir_path)
        return references

    def go_back(self, request: List[str]):
        self._pop_dir_path()
        return

    def go_to_entry(self, request: List[str]):
        if len(request) == 2:
            if request[0].upper() == 'TO':
                request.pop(0)
        if len(request) == 1:
            if request[0].upper() == 'HOME':
                self._pop_to_home()
                return
            if request[0].upper() == 'BACK' or request[0] == '..':
                self._pop_dir_path()
                return
            if request[0].isdigit():
                entry, index, entry_path = self._lookup_index_entry(request[0])
                new_path = os.path.realpath(entry_path)
                if os.path.isfile(new_path):
                    new_path = os.path.dirname(new_path)
                if not os.path.isdir(new_path):
                    raise ValueError(f'Not a directory: {self.rel_path(new_path)}')
                if not new_path.startswith(self._database_dir):
                    raise ValueError(f'Not in the database: {self.rel_path(new_path)}')
                self._push_dir_path(new_path)
                return
        if len(request) > 0:
            entry_name = ' '.join(request)
            dir_names = [
                entry
                for entry in os.listdir(self._cur_dir())
                if entry.lower() == entry_name.lower()
            ]
            if len(dir_names) > 0:
                new_path = os.path.realpath(os.path.join(self._cur_dir(), dir_names[0]))
                if not os.path.isdir(new_path):
                    raise ValueError(f'Not a directory: {self.rel_path(new_path)}')
                if not new_path.startswith(self._database_dir):
                    raise ValueError(f'Not in the database: {self.rel_path(new_path)}')
                self._push_dir_path(new_path)
                return
        self.help(['GO'])

    def _lookup_index_entry(self, index: str) -> Tuple[str, int, str]:
        if self._list_entries is None:
            raise ValueError(f'You need to list entries before using an index to it')
        if not index.isdigit():
            raise ValueError(f'Index "{index}" is not a number')
        index = int(index)
        if index < 1 or index > len(self._list_entries):
            raise ValueError(f'Index "{index}" out of range')
        return os.path.basename(self._list_entries[index-1]), index, self._list_entries[index-1]

    def help(self, request: List[str]):
        if len(request) > 0:
            for command in request:
                for entry in self._menu_items:
                    if command.upper() in entry[0]:
                        for line in entry[3]:
                            print(f'{red}{line}{black}')
            return
        for entry in self._menu_items:
            for line in entry[3]:
                print(f'{red}{line}{black}')

    def quit_app(self, request: List[str]):
        print(f'{blue}Goodbye!{black}')
        print()
        sys.exit(0)

    def rel_path(self, path: str = None) -> str:
        if path is None:
            path = self._cur_dir()
        return os.path.relpath(path, self._root_dir)

    def menu(self, request: List[str]):
        clear()
        print(f'{blue}File Manager{black}')
        print(f'{blue}============{black}')
        print()
        for entry in self._menu_items:
            print(f'{blue}{entry[0][0]} = {entry[1]}{black}')

    def run(self):
        self.menu([])
        while True:
            if self._last_error is not None:
                print(f'{red}Error> {self._last_error}{black}')
                self._last_error = None
            print()
            print(f'{green}Folder> [{len(self._dir_history)}] {self.rel_path()}{black}')
            print()
            request = input(f'{yellow}Action ? {black}')
            print()
            self._perform_request(request)

    def _perform_request(self, request: str):
        if len(request) > 0:
            request = request.split(' ')
            action = request[0].upper()
            for entry in self._menu_items:
                if action in entry[0]:
                    print(f'{green}Action> {entry[1]}{black}')
                    print()
                    try:
                        entry[2](request[1:])
                    except Exception as e:
                        self._last_error = e
                    return
            self._last_error = ValueError(f'Action "{action}" is not recognised')

    def _rename_link(self, index, entry_path, new_path, new_name):
        link_target = os.readlink(entry_path)
        if os.path.isdir(entry_path) or os.path.isfile(entry_path):
            os.symlink(link_target, new_path)
            if not os.path.lexists(new_path):
                raise ValueError(f'Failed to create "{new_name}"')
            self._list_entries[index - 1] = new_path
            self._list_entries.sort()
            os.remove(entry_path)
            if os.path.lexists(entry_path):
                raise ValueError(f'Failed to remove old entry "{entry_path}"')
            self._list_current_entries()
        else:
            raise ValueError(f'Not allowed to change the entry')

    def _rename_file_or_directory(self, index, entry_path, new_path, new_name):
        if os.path.isdir(entry_path):
            os.rename(entry_path, new_path)
            if not os.path.lexists(new_path) or os.path.lexists(entry_path):
                raise ValueError(f'Failed to rename to "{new_name}"')
            self._relink_references(entry_path, new_path)
            self._list_entries[index - 1] = new_path
            self._list_entries.sort()
            self._list_current_entries()
        elif os.path.isfile(entry_path):
            os.rename(entry_path, new_path)
            if not os.path.lexists(new_path) or os.path.lexists(entry_path):
                raise ValueError(f'Failed to rename to "{new_name}"')
            self._relink_references(entry_path, new_path)
            self._list_entries[index - 1] = new_path
            self._list_entries.sort()
            self._list_current_entries()
        else:
            raise ValueError(f'Not allowed to change the entry')

    def _relink_references(self, entry_path, new_path):
        """Relink references to entry_path to point to new_path"""
        real_path = os.path.realpath(entry_path)
        references = self._find_references(entry_path)
        for reference_path in references:
            if os.path.islink(reference_path):
                if os.path.realpath(reference_path) == real_path:
                    link_target = os.path.relpath(new_path, os.path.dirname(reference_path))
                    os.remove(reference_path)
                    if os.path.lexists(reference_path):
                        raise ValueError(f'Failed to remove the old link at {reference_path}')
                    os.symlink(link_target, reference_path)
                    if not os.path.lexists(reference_path):
                        raise ValueError(f'Failed to relink {reference_path} to {link_target}')

    def _list_entries_in_entry(self, entry_path, show_details=False, show_links=False):
        entries = sorted([os.path.join(entry_path, entry) for entry in os.listdir(entry_path)])
        self._list_relative_entries(entries, show_details=show_details, show_links=show_links)


def main():
    default_folder = os.path.join(os.getenv('HOME'), '.local', 'docman')
    if os.getenv('DOCMAN_HOME') is not None:
        default_folder = os.getenv('DOCMAN_HOME')
    parser = ArgumentParser(description='Document Manager')
    parser.add_argument('-f', '--folder', help='Main Folder', default=default_folder)
    args = parser.parse_args()
    try:
        file_manager = FileManager(root_dir=args.folder)
        file_manager.run()
    except Exception as ex:
        print(f'{red}Error> {ex}{black}')


if __name__ == '__main__':
    main()
