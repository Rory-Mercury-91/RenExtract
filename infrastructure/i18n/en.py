TRANSLATIONS = {
    "window": {
        "title": "🎮 {version}",
        "subtitle": "Intelligent Ren'Py Script Extraction"
    },
    "buttons_frame": {
        "pastilles": {
            "active": "🟢",
            "inactive": "⚫", 
            "unavailable": "🔴"
        }
    },
    "tabs": {
        "entree": "INPUT",
        "actions": "ACTIONS", 
        "outils": "TOOLS",
        "aide": "HELP"
    },
    "buttons": {
        "open_file": "Open File",
        "open_folder": "Open Folder",
        "next_file": "Next File",
        "next_file_last": "Last File",
        "next_file_disabled": "No Next File",
        "drag_drop": "Drag & Drop Mode",
        "ctrl_v": "Ctrl+V Mode",
        "extract_ui_characters": "Extract UI/Characters",
        "extract": "Extract",
        "reconstruct": "Reconstruct", 
        "reload": "Reload",
        "warnings": "Warnings",
        "check_tl_coherence": "Check TL Coherence",
        "unified_cleanup": "Cleanup TL",
        "auto_open": "Auto-Open : {status}",
        "temporary": "Temporary",
        "glossary": "Glossary",
        "backups": "Backups",
        "ok": "OK",
        "cancel": "Cancel",
        "quit": "Quit",
        "language": "Language", 
        "about": "About",
        "reset": "Reset",
        "theme": "Light Mode",
        "theme_dark": "Dark Mode",
        "debug_button": "Debug {status}",
        "no": "No",
        "yes": "Yes",
        "close": "Close",
        "complete_guide": "Complete Guide",
        "express_guide": "Express Guide",
        "execution_process": "Execution Process",
        "faq_about": "FAQ / About",
        "select_all": "Select All",
        "select_none": "Select None",
        "start_cleaning": "Start Cleaning",
        "add": "Add",
        "edit": "Edit",
        "modify": "Modify", 
        "delete": "Delete",
        "new": "New",
        "export": "Export",
        "import": "Import",
        "validate": "Validate",
        "save": "Save"
    },
    "status": {
        "no_file": "No file loaded",
        "ready": "Ready"
    },
    "help": {
        "title": "{version} - Help Center",
        "subtitle": "Choose the type of help you need:",
        "descriptions": {
            "complete_guide": "Comprehensive documentation covering all features",
            "express_guide": "The essentials in a few minutes to get started quickly",
            "execution_process": "Technical details of the extraction and reconstruction process",
            "faq_about": "Answers to frequently asked questions and application information"
        }
    },
    "clipboard": {
        "save_dialog": {
            "title": "Save Content",
            "main_title": "Save Content",
            "description": "Clipboard content detected.",
            "content_info": "Content Information",
            "content_stats": "{lines} line(s), {chars} character(s)",
            "save_options": "Save Options",
            "option_save": "Save this content to a file and continue",
            "option_continue": "Continue without saving",
            "option_cancel": "Cancel operation",
            "save_file_title": "Save Content",
            "error_title": "Save Error",
            "error_message": "Failed to save file:\n{error}",
            "empty": "Clipboard is empty",
            "error": "Error accessing clipboard"
        }
    },
    "coherence": {
        "select_tl_subfolder": "Select translation subfolder",
        "warning_not_tl_subfolder": "The selected folder is not a 'tl' subfolder",
        "check_done_no_issues": "Check completed, no issues",
        "check_done_with_issues": "Check completed, issues detected"
    },
    "input_manager": {
        "mode_changed": "Mode {mode_name} activated",
        "drag_drop_unavailable": "Drag & Drop unavailable on this platform",
        "error_configure_dnd": "Error configuring Drag & Drop",
        "error_configure_ctrl_v": "Error configuring Ctrl+V",
        "error_setup_dnd": "Error setting up Drag & Drop",
        "error_disable_dnd": "Error disabling Drag & Drop",
        "error_paste": "Error pasting",
        "ctrl_v_only": "Ctrl+V mode only active"
    },
    "file": {
        "open_title": "Open Ren'Py File",
        "select_folder_title": "Select folder containing .rpy files",
        "unsupported": "Unsupported file type. Only .rpy files are accepted."
    },
    "progress": {
        "processing": "Processing in progress..."
    },
    "info": {
        "lines_loaded": "Lines Loaded",
        "file_count_single": "1 file processed / 1 file",
        "file_count_multiple": "{current} file(s) processed / {total} files"
    },
    "about": {
        "window_title": "About {version}",
        "main_title": "🎮 {version}",
        "subtitle": "Advanced Translation Tool for Ren'Py Scripts",
        "description": "RenExtract is a specialized tool designed to simplify and optimize the translation process of games developed with the Ren'Py engine. It offers intelligent text extraction, automatic code protection, and an advanced validation system.",
        "features_title": "🌟 Key Features:",
        "features_list": [
            "Intelligent text extraction for translation",
            "Automatic protection of Ren'Py code",
            "Permanent glossary system",
            "Automatic coherence checking",
            "Drag & Drop and Ctrl+V support",
            "Multi-language interface",
            "Automatic backup management"
        ],
        "links_title": "🔗 Useful Links:",
        "links": {
            "github": "GitHub Repository",
            "github_desc": "Source code and releases",
            "documentation": "Documentation",
            "documentation_desc": "Full user manual",
            "bug_report": "Report a bug",
            "bug_report_desc": "Report an issue",
            "contact": "Contact developer",
            "contact_desc": "Support and questions"
        },
        "tech_info_title": "⚙️ Technical Information",
        "tech_info": {
            "version": "Version: {version}",
            "python": "Python: {python_version}",
            "platform": "Platform: {platform}",
            "interface": "Interface: Tkinter"
        },
        "close_button": "Close",
        "url_copied_title": "URL Copied",
        "url_copied_message": "The following URL has been copied to clipboard:\n{url}"
    },
    "content": {
        "dnd_available": "Drag & Drop mode active\n\nDrag your .rpy file here to get started.\n\nAuto-Open: {auto_status}\n\nAlternative solutions:\n• Use the 'Open File / Open Folder' buttons\n• Switch to Ctrl+V mode if available",
        "dnd_unavailable": "Drag & Drop unavailable\n\nTkinterdnd2 module is not installed.\n\nAuto-Open: {auto_status}\n\nAlternative solutions:\n• Use the 'Open File / Open Folder' buttons\n• Switch to Ctrl+V mode to paste content",
        "ctrl_v_mode": "Ctrl+V mode active\n\nUse Ctrl+V to paste content directly into this area.\n\nAuto-Open: {auto_status}\n\nAlternative solutions:\n• Use the 'Open File / Open Folder' buttons\n• Switch to Drag & Drop mode if available"
    },
    "extraction_ui": {
        "window_title": "Selection of texts to extract",
        "section_title": "Texts of type: {origine}",
        "separator_characters_selectionables": "Selectable character texts ({count}):",
        "separator_selectionables": "Selectable texts ({count}):",
        "separator_auto_inputs": "Automatically selected input fields ({count}):",
        "separator_auto_characters": "Automatically selected texts ({count}):",
        "validate_button": "Confirm Selection"
    },
    "cleanup_handler": {
        "module_unavailable": {
            "title": "Module Unavailable",
            "message": "The Unified Cleanup module is not available.\n"
                      "Make sure the core/sup_lignes_orphelines.py file exists\n"
                      "and that all dependencies are installed."
        },
        "dialogs": {
            "select_lint_file": "Select lint.txt file",
            "select_game_folder": "Select game folder",
            "select_tl_folder": "Select tl folder",
            "confirm_unified_cleanup": "Confirm Unified Cleanup",
            "language_selection_title": "Unified Cleanup - Language Selection",
            "cleaning_success": "Cleanup successful",
            "cleaning_error": "Cleanup error"
        },
        "language_scan": {
            "scan_error_title": "Scan Error",
            "scan_error_message": "Failed to scan for available languages.\n"
                                 "Error: {error}\n\n"
                                 "Folder analyzed: {folder}\n"
                                 "Content: {content}",
            "no_languages_title": "No Languages Found",
            "no_languages_message": "No translation languages found in folder:\n{folder}\n\n"
                                   "Folder content:\n{content}\n\n"
                                   "Make sure the tl folder contains language subfolders\n"
                                   "with .rpy files."
        },
        "confirmation": {
            "message": "Unified cleanup for languages: {languages}\n\n"
                      "Lint.txt file: {lint_file}\n"
                      "Game folder: {game_folder}\n"
                      "Tl folder: {tl_folder}\n\n"
                      "Do you want to proceed?"
        },
        "results": {
            "success_message": "Unified cleanup successfully completed!\n\n"
                              "Languages processed: {languages_processed}\n"
                              "Files processed: {files_processed}\n"
                              "Blocks removed: {blocks_removed}\n"
                              "Execution time: {execution_time}",
            "error_message": "Unified cleanup error:\n{errors}",
            "log_success": "Unified cleanup completed: {blocks_removed} blocks removed in {execution_time}",
            "log_error": "Unified cleanup error: {error}"
        },
        "language_selection": {
            "dialog_title": "Unified Translation Cleanup",
            "dialog_subtitle": "Select languages to clean:",
            "languages_detected": "{count} language(s) detected | Automatic backup enabled",
            "language_item_info": "Translation language | Lint.txt + Correspondence Cleanup",
            "tip_bottom": "Tip: Unified cleanup combines two methods for optimal results",
            "no_selection_warning": "Please select at least one language to clean."
        },
        "processing": {
            "in_progress": "Unified cleanup in progress...",
            "status_message": "Unified cleanup for {count} language(s)"
        },
        "execution_time": {
            "seconds": "{duration:.1f} seconds",
            "minutes_seconds": "{minutes}m {seconds}s",
            "hours_minutes": "{hours}h {minutes}m"
        },
        "report": {
            "title": "RENEXTRACT CLEANUP REPORT",
            "separator": "=" * 60,
            "fields": {
                "game": "Game: {game_name}",
                "date": "Date: {date}",
                "execution_time": "Execution time: {time}",
                "languages_processed": "Languages processed: {count}",
                "files_processed": "Files processed: {count}",
                "blocks_removed": "Blocks removed: {count}"
            },
            "sections": {
                "method_summary": "SUMMARY BY CLEANUP METHOD",
                "language_detail": "DETAILS PER LANGUAGE",
                "lint_cleanup": "Lint.txt cleanup: {count} blocks removed",
                "string_cleanup": "String-based cleanup: {count} blocks removed",
                "total_cleanup": "Total: {count} blocks removed",
                "language_files": "Files processed: {count}",
                "language_blocks": "Blocks removed: {count}",
                "by_lint": "- By lint.txt: {count}",
                "by_correspondence": "- By correspondence: {count}"
            },
            "creation_success": "Cleanup report created: {filename}",
            "creation_error": "Failed to create cleanup report",
            "auto_open_success": "Report auto-opened: {path}",
            "auto_open_error": "Failed to auto-open report: {error}"
        }
    },
    "backup": {
        "window_title": "Backup Manager - {filename}",
        "no_file": "No file selected",
        "no_file_message": "Please load a file first before accessing backups.",
        "game_label": "Game: {game_name}",
        "auto_backup_info": "Automatic backups created at each extraction",
        "searching": "Searching for backups...",
        "refreshing": "Refreshing...",
        "no_backups_found": "No backups found for game '{game_name}'.\n\nBackups are created automatically during extractions.",
        "created_label": "Created on:",
        "size_label": "Size:",
        "age_label": "Age:",
        "restore_button": "Restore",
        "delete_button": "Delete",
        "most_recent_badge": "Most Recent",
        "safety_badge": "Safety Backup",
        "refresh_button": "Refresh",
        "close_button": "Close",
        "restore_confirm_title": "Confirm Restore",
        "restore_confirm_message": "Restore backup:\n'{name}'\n\nGame: {game}\nCreated on: {created}\n\nThis action will replace the current file.",
        "restore_success_title": "Restore Successful",
        "restore_success_message": "Backup '{name}' successfully restored.\n\nGame: {game}\nCreated on: {created}\n\nDo you want to delete this backup?",
        "restore_error_title": "Restore Error",
        "restore_error_message": "Error restoring '{name}':\n{error}",
        "restore_critical_error_title": "Critical Error",
        "restore_critical_error_message": "Critical error during restore:\n{error}",
        "delete_confirm_title": "Confirm Deletion", 
        "delete_confirm_message": "Permanently delete backup:\n'{name}'\n\nGame: {game}\nCreated on: {created}\nSize: {size:.2f} MB\n\nThis action is irreversible.",
        "delete_success_title": "Deletion Successful",
        "delete_success_message": "Backup '{name}' successfully deleted.",
        "delete_error_title": "Deletion Error",
        "delete_error_message": "Error deleting '{name}':\n{error}",
        "errors": {
            "load_error": "Load Error",
            "load_error_message": "Error loading backups for {filepath}: {error}"
        }
    },
    "file_types": {
        "text_files": "Text File (*.txt)",
        "all_files": "All Files (*.*)"
    },
    "export": {
        "glossary_header": "RenExtract Glossary - Exported on",
        "glossary_format": "Format: Original => Translation"
    },
    "titles": {
        "error_title": "Error",
        "warning_title": "Warning", 
        "info_title": "Information",
        "success_title": "Success",
        "confirm_title": "Confirmation",
        "validation_success": "Validation Successful",
        "validation_failed": "Validation Failed"
    },
    "interface": {
        "save_mode": {
            "title": "Save Mode",
            "description": "How do you want to save the reconstructed file?",
            "new_file": {
                "title": "New File",
                "description": "Create a new file with a different name"
            },
            "overwrite": {
                "title": "Overwrite Original", 
                "description": "Replace the original file with the reconstructed version"
            },
            "cancel": "Cancel"
        },
        "progress": {
            "title": "Processing in progress...",
            "processing": "Processing...",
            "initializing": "Initializing..."
        },
        "status_bar": {
            "separator": "|"
        },
        "validation": {
            "dialog_title": "Validation Results"
        }
    },
    "notification_manager": {
        "fallback": {
            "title": "Information",
            "unknown_type": "Unknown notification type",
            "priority_too_low": "Toast ignored (priority {priority} too low)"
        },
        "errors": {
            "notify_error": "Error in notify()",
            "handle_toast_error": "Error _handle_toast()",
            "show_toast_immediate_error": "Error _show_toast_immediate()",
            "handle_toast_priority_error": "Error _handle_toast_priority()",
            "create_toast_window_error": "Error _create_toast_window()",
            "setup_toast_events_error": "Error _setup_toast_events()",
            "calculate_toast_position_error": "Error _calculate_toast_position()",
            "reposition_all_toasts_error": "Error _reposition_all_toasts()",
            "reposition_individual_error": "Error individual toast repositioning",
            "auto_close_error": "Error auto-closing toast",
            "remove_toast_error": "Error _remove_toast()",
            "handle_modal_error": "Error _handle_modal()",
            "handle_confirm_error": "Error _handle_confirm()",
            "handle_status_error": "Error _handle_status()",
            "cleanup_error": "Error cleaning up NotificationManager",
            "status_update_impossible": "Status update impossible"
        }
    },
    "tutorial": {
        "title": "Complete Guide - {version}",
        "subtitle": "Master all aspects of RenExtract",
        "express_title": "Express Guide - {version}",
        "express_subtitle": "The essentials in a few minutes",
        "non_blocking_notice": "This window is non-blocking: you can use the application in parallel!",
        "understood_button": "Understood!",
        "collapse_all_button": "Collapse All",
        "expand_all_button": "Expand All",
        "content": {
            "guide_complet": {
                "interface": {
                    "title": "User Interface",
                    "overview": "The RenExtract interface is divided into functional areas for optimal use:",
                    "header_section": "Header Section",
                    "header_quit_desc": "• 'Quit' button: Closes the application cleanly",
                    "header_language_desc": "• 'Language' button: Changes the interface language (FR/EN/DE)",
                    "header_theme_desc": "• 'Theme' button: Switches between light and dark modes",
                    "header_about_desc": "• 'About' button: Information about the application",
                    "header_debug_desc": "• 'Debug' button: Activates/deactivates debug mode",
                    "info_zone_section": "Information Zone",
                    "info_zone_split_desc": "• Split display: File path on the left, line count on the right",
                    "info_zone_single_desc": "• Single file mode: Information on the current file",
                    "info_zone_folder_desc": "• Folder mode: Progress 'X file(s) processed / Y files'",
                    "info_zone_empty_desc": "• Empty status: 'No file loaded' when nothing is open",
                    "file_buttons_section": "File Buttons (INPUT tab)",
                    "btn_open_file_desc": "• 'Open File': Selects a single .rpy file",
                    "btn_open_folder_desc": "• 'Open Folder': Processes all .rpy files in a folder",
                    "btn_next_file_desc": "• 'Next File': Moves to the next file in folder mode",
                    "btn_input_mode_desc": "• Input modes: Drag & Drop or Ctrl+V with color indicators",
                    "btn_backups_desc": "• 'Backups': Manages automatic backups",
                    "btn_reset_desc": "• 'Reset': Resets the application to zero",
                    "action_buttons_section": "Action Buttons (ACTIONS tab)",
                    "btn_extract_desc": "• 'Extract': Starts the extraction of translatable texts",
                    "btn_reconstruct_desc": "• 'Reconstruct': Reassembles the file with translations",
                    "btn_verify_desc": "• 'Reload': Reloads the reconstructed file for verification",
                    "tool_buttons_section": "Tool Buttons (TOOLS tab)",
                    "btn_warnings_desc": "• 'Warnings': Opens the translation warnings file",
                    "btn_temp_desc": "• 'Temporary Folder': Accesses temporary files",
                    "btn_auto_open_desc": "• 'Auto-Open': Activates/deactivates automatic file opening",
                    "btn_glossary_desc": "• 'Glossary': Manages the translation dictionary",
                    "btn_help_desc": "• Help buttons: Guides and FAQ",
                    "content_zone_section": "Main Content Area",
                    "content_zone_features_desc": "• Main text area with syntax highlighting and scrolling",
                    "content_zone_dnd_desc": "• Drag & Drop support when available (tkinterdnd2 module)",
                    "content_zone_ctrlv_desc": "• Ctrl+V mode for direct content pasting",
                    "content_zone_unavailable_desc": "• Contextual help messages depending on the active mode",
                    "content_zone_loading_desc": "• Displays file content with automatic numbering"
                },
                "workflow": {
                    "title": "Recommended Workflow",
                    "step_1": "1. Load your .rpy file (Drag & Drop, Ctrl+V, or buttons)",
                    "step_2": "2. Start extraction to identify translatable texts",
                    "step_3": "3. Edit the generated temporary file with your translations",
                    "step_4": "4. Reconstruct the final file with your changes",
                    "step_5": "5. Reload it to check the result",
                    "step_6": "6. Gradually enrich the glossary",
                    "step_7": "7. Backups are automatically created at each step"
                },
                "files": {
                    "title": "File Organization",
                    "where": "• 'temp/' folder: Temporary extraction files",
                    "temp": "• 'notranslate/' folder: Identified non-translatable files",
                    "notranslate": "• 'translated/' folder: Reconstructed final files",
                    "translated": "• 'warnings/' folder: Detected warnings and issues",
                    "warnings": "• 'configs/' folder: Configuration and glossary",
                    "configs": "• 'backup/' folder: Automatic backups per game",
                    "backups": "• All folders are created automatically",
                    "access": "• Dedicated buttons for quick access to each folder"
                },
                "advanced": {
                    "title": "Advanced Features",
                    "glossary": "• Permanent glossary for reusing your recurring translations",
                    "validation": "• Automatic validation of Ren'Py syntax",
                    "notifications": "• Notification system with colored toasts and priorities"
                },
                "tips": {
                    "title": "Usage Tips",
                    "debug": "• Activate debug mode for more detailed information",
                    "restore": "• Backups allow you to revert in case of error",
                    "dnd": "• Drag & Drop works from file explorer",
                    "glossary": "• Build your glossary gradually to save time",
                    "help": "• Consult specialized guides as needed"
                },
                "shortcuts": {
                    "title": "Shortcuts and Modes",
                    "dnd": "• Drag & Drop: Drag your files directly into the area",
                    "ctrlv": "• Ctrl+V: Paste script content directly",
                    "actions": "• Buttons are organized by tabs for clear navigation"
                },
                "faq": {
                    "title": "Frequently Asked Questions",
                    "where_translated": "• Translated files are located in the 'translated/' folder",
                    "validation_error": "• Validation errors are detailed in notifications",
                    "custom_glossary": "• You can import/export your glossary",
                    "reset": "• The 'Reset' button deletes everything and restarts",
                    "when_temp_deleted": "• If temporary files are deleted, restart extraction"
                }
            },
            "quick_workflow": "Quick Workflow",
            "quick_steps": "1. Load → 2. Extract → 3. Translate → 4. Reconstruct",
            "shortcuts": "Useful Shortcuts",
            "drag_drop_info": "• Drag & Drop your .rpy files directly",
            "ctrl_v_info": "• Use Ctrl+V to paste content",
            "buttons_info": "• Buttons organized by thematic tabs",
            "new_features": "New Features",
            "glossary_brief": "• Permanent glossary for your translations",
            "architecture_brief": "• Modular architecture and redesigned UI",
            "notifications_brief": "• Smart notifications with priorities",
            "express_tip": "For more details, consult the complete guide in the Help menu!"
        }
    },
    "help_specialized": {
        "execution_process": {
            "title": "Detailed Execution Process",
            "subtitle": "Understanding RenExtract's Inner Workings",
            "understood_button": "Process Understood!",
            "sections": {
                "objective": {
                    "title": "Process Objective",
                    "content": {
                        "0": "RenExtract automates the extraction and reconstruction of Ren'Py scripts for translation.",
                        "1": "The process preserves code integrity while isolating translatable texts.",
                        "2": "Each step is validated to ensure compatibility with the Ren'Py engine."
                    }
                },
                "workflow": {
                    "title": "Processing Steps",
                    "content": {
                        "0": "• Phase 1: Source file syntax analysis",
                        "1": "• Phase 2: Identification of translatable patterns",
                        "2": "• Phase 3: Extraction into a structured temporary file",
                        "3": "• Phase 4: Integration of translations",
                        "4": "• Phase 5: Reconstruction with syntax validation",
                        "5": "• Phase 6: Generation of the final file and saving"
                    }
                },
                "protection": {
                    "title": "Code Protection",
                    "content": {
                        "0": "• Python code blocks are fully preserved",
                        "1": "• Conditional structures (if, while, for) are protected",
                        "2": "• Variable definitions and functions remain intact",
                        "3": "• Technical comments are maintained",
                        "4": "• Only texts intended for the player are extracted"
                    }
                },
                "validation": {
                    "title": "Quality Controls",
                    "content": {
                        "0": "• Ren'Py syntax verification before and after processing",
                        "1": "• Coherence check of dialogue structures",
                        "2": "• Validation of substitution patterns",
                        "3": "• Detection of problematic characters",
                        "4": "• Detailed error report in case of issue"
                    }
                },
                "structure": {
                    "title": "Structure of Generated Files",
                    "content": {
                        "0": "• Temp file: Structured formatting for editing",
                        "1": "• Clear separation between original text and translation",
                        "2": "• Automatic numbering for tracking",
                        "3": "• Contextual comments to aid translation",
                        "4": "• Preservation of references and internal links"
                    }
                },
                "tips": {
                    "title": "Optimization Tips",
                    "content": {
                        "0": "• Use the glossary for recurring translations",
                        "1": "• Always check the reconstructed file before use",
                        "2": "• Keep a backup copy of your original files",
                        "3": "• Activate debug mode for more details on the process",
                        "4": "• Consult warnings to identify potential improvements"
                    }
                }
            }
        },
        "faq_about": {
            "title": "FAQ and About",
            "subtitle": "Frequently Asked Questions and Information about RenExtract",
            "understood_button": "Got It!",
            "sections": {
                "faq": {
                    "title": "Frequently Asked Questions",
                    "content": {
                        "0": "Q: Where are my translated files saved?",
                        "1": "A: In the 'translated/' folder, created automatically.",
                        "2": "",
                        "3": "Q: What to do if validation fails?",
                        "4": "A: Check the warnings and fix the reported syntax errors.",
                        "5": "",
                        "6": "Q: How do I save my glossary?",
                        "7": "A: Use the export/import buttons in the glossary manager.",
                        "8": "",
                        "9": "Q: The application crashes during processing?",
                        "10": "A: Activate debug mode and check logs to identify the issue.",
                        "11": "",
                        "12": "Q: Can I process multiple files at once?",
                        "13": "A: Yes, use 'Open Folder' to process all .rpy files in a directory."
                    }
                },
                "tips": {
                    "title": "Tips and Tricks",
                    "content": {
                        "0": "• Back up your glossary regularly to reuse your translations",
                        "1": "• Use drag & drop mode for a faster workflow",
                        "2": "• The 'Reset' button deletes everything - use it to start over",
                        "3": "• Automatic backups allow you to go back",
                        "4": "• Check the warnings folder to improve your translations",
                        "5": "• Debug mode shows more information in the console"
                    }
                }
            }
        }
    },
    "app_controller": {
        "file_operations": {
            "file_loaded_success": "File {filename} loaded successfully",
            "folder_processing": "Opening folder...",
            "folder_analysis_complete": "Folder analysis complete",
            "dropped_folder_analysis": "{count} more .rpy files detected in this folder",
            "dropped_folder_suggestion_few": "Tip: {count} more .rpy files detected in this folder",
            "dropped_folder_suggestion_many": "Tip: {count} more .rpy files detected (use 'Open Folder' to process all)",
            "renpy_structure_detected": "Ren'Py structure detected",
            "clipboard_content_too_short": "Content too short for processing",
            "clipboard_loading_cancelled": "Clipboard loading cancelled by user",
            "clipboard_content_saved_loaded": "Clipboard content saved and loaded: {count} lines",
            "clipboard_unexpected_case": "Unexpected case in load_from_clipboard"
        },
        "processing": {
            "extraction_started": "Extraction in progress...",
            "reconstruction_started": "Reconstruction in progress...",
            "post_processing_ellipsis": "Post-processing: {count} [...] corrected in ...",
            "coherence_check_started": "Coherence check in progress...",
            "file_modified_check": "Translation file not modified since extraction (timestamp: {timestamp})",
            "file_modification_detected": "Translation file modified since extraction - reconstruction allowed",
            "file_dialogue_missing": "Dialogue file no longer exists: {path}",
            "modification_check_conditions_not_met": "File modification check - conditions not met"
        },
        "language_management": {
            "language_interface_success": "Interface in {language_name}"
        },
        "validation": {
            "validation_with_values": "Validation with: extracted={extracted}, asterix={asterix}, empty={empty}",
            "extracted_count_zero": "extracted_count is 0, this seems wrong",
            "recalculated_from_file": "extracted_count recalculated from file: {count}",
            "validation_failed_continue": "Validation failed, continue anyway?",
            "validation_error_continue": "Validation error before reconstruction: {error}"
        },
        "errors": {
            "file_open_error": "File open error",
            "folder_open_error": "Folder open error",
            "drag_drop_error": "D&D file error",
            "clipboard_load_error": "Clipboard load error",
            "clipboard_dialog_error": "Dialog save error: {error}",
            "extraction_error": "Extraction error",
            "reconstruction_error": "Reconstruction error",
            "reload_error": "Reload error",
            "theme_toggle_error": "Error toggling theme: {error}",
            "auto_open_toggle_error": "Error toggling auto-open",
            "language_change_error": "Language change error: {error}",
            "language_menu_error": "Language menu error",
            "interface_recreation_error": "Error recreating interface: {error}",
            "theme_application_error": "Error applying theme: {error}",
            "language_change_critical": "Critical error recreating interface: {error}",
            "debug_toggle_error": "Error toggling debug mode: {error}",
            "about_display_error": "Error displaying 'About'",
            "help_display_error": "Error displaying help",
            "glossary_open_error": "Glossary open error",
            "backup_manager_error": "Backup manager error",
            "warnings_open_error": "Warnings open error",
            "temporary_open_error": "Temporary open error",
            "reset_error": "Reset error",
            "refresh_error": "Refresh error",
            "app_close_error": "App close error",
            "next_file_error": "Next file error",
            "folder_open_system_error": "Cannot open folder {path}: {error}",
            "ui_extraction_critical": "Exception: {error}",
            "post_processing_error": "Post-processing error: {error}",
            "ellipsis_correction_error": "Ellipsis correction error: {error}",
            "old_warnings_cleanup_error": "Error cleaning old warnings: {error}",
            "temp_folders_cleanup_error": "Error cleaning folders: {error}",
            "file_load_error": "File load error: {error}",
            "dropped_folder_analysis_error": "Error in D&D folder analysis: {error}"
        },
        "debug": {
            "debug_mode_enabled": "Debug mode enabled",
            "debug_mode_disabled": "Debug mode disabled",
            "debug_detailed_logs_visible": "Debug mode enabled - Detailed logs are now visible",
            "debug_normal_logs_return": "Debug mode disabled - Returning to normal logs",
            "debug_mode_activated": "Debug mode activated",
            "debug_mode_deactivated": "Debug mode deactivated",
            "debug_toggle_error_message": "Error toggling debug mode"
        },
        "notifications": {
            "language_menu_error_fallback": "Error displaying language menu",
            "about_fallback": "{version}\nRen'Py Translation Tool",
            "success_notification_error": "Success notification error: {error}",
            "theme_change_error_message": "Error changing theme"
        },
        "file_management": {
            "last_directory_updated_dnd": "last_directory updated via D&D: {directory}",
            "folder_dnd_contains_rpy": "D&D folder contains {count} more .rpy files",
            "renpy_structure_detected_dnd": "Ren'Py structure detected via D&D: {path}",
            "file_loaded_anonymized": "File loaded: {path} in {time:.2f}s",
            "clipboard_counter_generated": "Clipboard counter generated: {counter}",
            "virtual_file_created": "Virtual file created: {name}",
            "clipboard_content_loaded": "Clipboard content loaded: {path}",
            "folder_files_valid": "File ignored: {filename} - {error}",
            "backup_failed": "Backup failed: {error}",
            "extraction_file_timestamp": "Extraction file timestamp saved: {timestamp}",
            "dialogue_file_path": "Dialogue file path: {path}",
            "dialogue_file_not_found": "Dialogue file not found or does not exist: {path}",
            "next_file_loaded": "Next file loaded: {path}",
            "folder_deleted": "Folder {type} deleted: {name}"
        }
    },
    "coherence_checker": {
        "analysis": {
            "file_not_found": "File not found: {filepath}",
            "system_error": "System error: {error}"
        },
        "issues": {
            "missing_old": "NEW line without matching OLD",
            "analysis_error": "Analysis error: {error}"
        },
        "warning_file": {
            "unique_file_report": "SINGLE FILE REPORT",
            "game": "Game",
            "analyzed_file": "Analyzed File",
            "date": "Date",
            "issues_detected": "Issues detected: {count}",
            "line_prefix": "Line {line}",
            "old_prefix": "OLD",
            "new_prefix": "NEW", 
            "content_prefix": "CONTENT",
            "summary": "SUMMARY",
            "issues_count_format": "• {count} issue(s) of type {type}",
            "warning_note": "⚠️ Note: These issues can affect the correct functioning of the script.",
            "tip_note": "💡 Tip: Fix these issues before reconstructing the file."
        },
        "report": {
            "title": "RENEXTRACT COHERENCE REPORT",
            "analyzed_folder": "Analyzed Folder",
            "date": "Date",
            "problems_detected": "Problems detected",
            "summary_title": "DETAILED SUMMARY",
            "total_problems": "Total problems detected: {total}",
            "technical_note": "Technical Note: Variables with translation functions (e.g., [TEMP1!t], [VAR!u]) have been normalized for comparison.",
            "technical_explanation": "If you see [TEMP1!t] in your files but the report shows [TEMP1], this is normal - functions !t, !u, !l, !c are ignored."
        },
        "issue_types": {
            "variables_inconsistent": "Inconsistent Variables",
            "tags_inconsistent": "Inconsistent Tags", 
            "placeholders_inconsistent": "Inconsistent Placeholders",
            "quote_problems": "Quote Problems",
            "other_problems": "Other Problems"
        }
    },
    "extract_ui_characters": {
        "file_dialog": {
            "save_title": "Where to save the generated .rpy file?",
            "file_types": {
                "renpy_script": "Ren'Py Script (*.rpy)",
                "all_files": "All Files (*.*)"
            }
        },
        "messages": {
            "cancelled_by_user": "Save cancelled by user.",
            "file_auto_opened": "File auto-opened: {save_path}",
            "auto_open_disabled": "Auto-open disabled in settings"
        },
        "notifications": {
            "extraction_started": "UI/Character extraction in progress...",
            "extraction_success": "UI/Character extraction completed successfully",
            "extraction_error": "UI/Character extraction error: {error}"
        }
    },
    "extraction": {
        "validation": {
            "file_invalid_path": "Invalid file path",
            "file_not_found": "File not found: {filepath}",
            "file_not_file": "Path does not refer to a file: {filepath}",
            "file_too_large": "File too large ({size_mb:.1f} MB, max {max_mb} MB)",
            "file_empty": "Empty file",
            "file_size_error": "Error reading size: {error}",
            "permissions_read": "Insufficient read permissions",
            "permissions_check_error": "Error checking permissions: {error}",
            "unsupported_extension": "Unsupported file extension",
            "wrong_renpy_structure": "Wrong Ren'Py structure",
            "missing_language_folder": "Missing language folder after tl/",
            "renpy_structure_not_detected": "Ren'Py structure not detected",
            "file_empty_content": "File with no content",
            "suspicious_content": "Suspicious content detected",
            "encoding_error": "File encoding error",
            "read_error": "Read error: {error}",
            "dangerous_filename": "Dangerous character '{char}' in filename",
            "unexpected_error": "Unexpected error: {error}"
        },
        "errors": {
            "invalid_content": "Invalid or missing file content",
            "load_file_error": "Error loading file",
            "extraction_error": "Critical error during extraction",
            "save_files_error": "Error saving files",
            "duplicate_management_error": "Error in duplicate management",
            "asterix_detection_error": "Error in asterisk detection",
            "glossary_protection_error": "Error in glossary protection",
            "code_mapping_error": "Error creating mapping",
            "empty_text_protection_error": "Error protecting empty texts",
            "dialogue_extraction_error": "Error in dialogue extraction",
            "placeholder_application_error": "Error applying placeholders"
        },
        "fallbacks": {
            "default_name": "untitled_file"
        }
    },
    "glossary": {
        "title": "Glossary Manager",
        "search": "Search:",
        "entries_title": "Glossary Entries",
        "edit_title": "Editing",
        "original_label": "Original Text",
        "translation_label": "Translation",
        "labels": {
            "original": "Original Text:",
            "translation": "Translation:",
            "search": "Search:",
            "entries_count": "{count} Entry/Entries",
            "statistics": "Statistics"
        },
        "messages": {
            "entries_count": "{count} Entry/Entries",
            "empty_fields": "Please fill in both fields.",
            "add_error": "This entry already exists.",
            "no_selection": "Please select an entry to edit.",
            "modify_error": "Error modifying.",
            "no_selection_delete": "Please select an entry to delete.",
            "confirm_delete": "Delete entry:\n'{original}' → '{translation}'?",
            "export_error": "Error exporting.",
            "import_mode": "Merge with existing glossary?\n\nYes = Merge\nNo = Replace entirely",
            "import_error": "Error importing.",
            "validation_success": "Glossary validated: no issues detected.",
            "validation_issues": "{count} issue(s) detected in glossary.",
            "validation_issues_text": "Issue details:\n{issues}",
            "new_entry_added": "New entry added: '{original}' → '{translation}'",
            "entry_updated": "Entry updated: '{original}' → '{translation}' (was: '{old_translation}')",
            "entry_removed": "Entry removed: '{original}' → '{translation}'",
            "glossary_loaded": "Glossary loaded: {count} entries",
            "new_glossary_created": "New glossary created",
            "glossary_saved": "Glossary saved: {count} entries",
            "glossary_export_success": "Glossary exported to: {filepath}",
            "glossary_import_success": "Glossary imported: {count} entries from {filepath}",
            "line_ignored_format": "Line ignored (wrong format) line {line_num}: {line}",
            "no_glossary_terms": "No glossary terms - protection ignored",
            "exact_protection_start": "Glossary protection with exact match: {count} terms",
            "term_protected": "Term protected (exact): '{original}' → {placeholder} ({count}x line {line})",
            "exact_protection_complete": "Exact glossary protection complete: {placeholders} placeholders, {replacements} replacements",
            "line_modified": "Line {line} modified by glossary protection"
        },
        "empty_fields_title": "Empty Fields",
        "add_error_title": "Entry Exists",
        "no_selection_title": "No Selection",
        "modify_error_title": "Modification Error",
        "no_selection_delete_title": "No Selection",
        "confirm_delete_title": "Confirm Deletion",
        "export_title": "Export Glossary",
        "export_error_title": "Export Error",
        "import_title": "Import Glossary",
        "import_mode_title": "Import Mode",
        "import_error_title": "Import Error",
        "validation_success_title": "Validation Successful",
        "validation_issues_title": "Issues Detected",
        "validation_issues_text_title": "Issue Details",
        "validation": {
            "empty_original": "Empty original term",
            "empty_translation": "Empty translation for '{original}'",
            "duplicate_translation": "Duplicate translation '{translation}' for '{original}' (also used by '{duplicates}')",
            "short_term": "Very short term '{original}' - risk of unwanted substitutions",
            "special_characters": "Term '{original}' contains special characters - check result",
            "validation_error": "Validation error: {error}",
            "term_very_short": "Term very short '{original}' - risk of unwanted substitutions",
            "term_special_chars": "Term '{original}' contains special characters - check result",
            "term_substring": "'{original}' is a substring of '{other_original}' - processing order matters",
            "translation_empty": "Translation empty for '{original}'",
            "translation_duplicate": "Translation '{translation}' used for multiple terms: {terms}"
        },
        "help": {
            "title": "Glossary Help",
            "subtitle": "Guide to using the glossary system",
            "button_tooltip": "Glossary Help",
            "sections": {
                "principe": "Operating Principle",
                "principe_content": "The glossary allows automatic replacement of recurring terms with their translation during extraction. Terms are protected by placeholders and automatically restored with the translation during reconstruction.",
                "exemple": "Example of Use",
                "exemple_content": "If you add 'wish' → 'souhaite', 'I wish you well' will automatically become 'I souhaite you well' after reconstruction, even if the original text contained other words like 'wishes' or 'wishful' which are not affected.",
                "ajouter": "Adding Terms",
                "ajouter_content": "Use the 'Add' button to create new entries. Enter the original term in English and its German translation. The match is exact (case-sensitive).",
                "usage": "Usage",
                "usage_content": "The glossary is automatically applied during extraction if the option is enabled. Terms are replaced by placeholders (GLOSS001, GLOSS002...) and restored with the translation during reconstruction.",
                "bonnes_pratiques": "Best Practices",
                "bonnes_pratiques_content": "• Use full terms instead of fragments\n• Avoid overly short terms (less than 3 characters)\n• Ensure your translations are consistent\n• Test on a few files before massive use",
                "import_export": "Import/Export",
                "import_export_content": "You can export your glossary to a text file to share or back it up, and import existing glossaries. Format: 'Original => Translation' (one entry per line).",
                "validation": "Validation",
                "validation_content": "Use the validation function to detect potential issues: duplicates, overly short terms, special characters, etc. Correct the reported errors to optimize efficiency."
            }
        }
    },
    "reconstruction": {
        "validation": {
            "path_invalid": "Invalid path",
            "path_not_renpy_structure": "Path does not match Ren'Py structure",
            "path_permissions_read": "Insufficient read permissions",
            "path_permissions_write": "Insufficient write permissions",
            "path_permissions_dir_read": "Insufficient folder read permissions",
            "path_permissions_dir_write": "Insufficient folder write permissions"
        },
        "errors": {
            "invalid_content": "Invalid or missing file content",
            "original_path_not_defined": "Original file path not defined",
            "original_path_not_string": "Original file path is not a string",
            "original_not_rpy": "Original file does not have .rpy extension",
            "invalid_save_path": "Invalid save path: {error}",
            "invalid_save_content": "Invalid or missing content to save",
            "parent_directory_error": "Failed to create parent directory: {error}",
            "save_error": "Error saving: {error}",
            "missing_mapping_files": "Missing files in {folder}:\n• {file1}\n• {file2}",
            "missing_dialogue_file": "Missing dialogue file: {file}",
            "comment_original_error": "Failed to comment original file: {error}",
            "content_missing": "File content or original path missing",
            "critical_error": "Critical error: {error}",
            "validation_error": "Validation error: {error}"
        },
        "validation_errors": {
            "mismatch_count": "Incorrect number of translations: {provided} provided, {expected} expected",
            "asterix_warning": "{count} expressions detected between asterisks - check other.txt",
            "empty_warning": "{count} empty texts/spaces detected - check empty.txt"
        }
    },
    "sup_lignes_orphelines": {
        "orphan_line_cleaner": {
            "init": "Initializes the orphan block cleaner",
            "create_backup": "Creates a backup of the file before cleaning",
            "get_statistics": "Returns cleaning statistics"
        },
        "string_based_cleaner": {
            "init": "Initializes the string-based cleaner",
            "create_backup": "Creates a backup of the file before cleaning"
        },
        "unified_cleaner": {
            "init": "Initializes the unified cleaner"
        },
        "line_detection": {
            "block_start_description": "Checks if a line is the start of a translation block",
            "extract_id_description": "Extracts the ID of a translation block",
            "old_line_description": "Checks if a line is an OLD line",
            "new_line_description": "Checks if a line is a NEW line",
            "old_with_text_description": "Checks if a line is an old line with text",
            "new_with_text_description": "Checks if a line is a new line with text"
        },
        "errors": {
            "file_not_found": "File not found: {file_path}",
            "lint_file_not_found": "Lint.txt file not found: {lint_file_path}",
            "language_processing_error": "Error processing language {language}: {error}",
            "general_unified_error": "General unified cleanup error: {error}",
            "language_folder_not_found": "Language folder not found: {language_folder}"
        },
        "patterns": {
            "line_marker": "* line",
            "id_marker": "(id ",
            "game_comment": "# game/",
            "todo_comment": "# TODO:",
            "old_prefix": "old ",
            "new_prefix": "new "
        }
    },
    "validation": {
        "success_message": "{file_type} successfully validated (confidence: {confidence}%). {patterns_count} Ren'Py patterns detected.",
        "failed_message": "Validation failed:\n{errors}",
        "warnings_title": "Warnings:",
        "errors_title": "Errors:",
        "file_not_found": "File not found",
        "non_rpy_extension": "No .rpy extension detected",
        "non_utf8_encoding": "No UTF-8 encoding detected",
        "read_error": "Read error: {error}",
        "file_empty": "Empty file",
        "validation_error": "Validation error: {error}",
        "low_confidence": "Low confidence level for validation",
        "backup_success": "Backup successfully created",
        "backup_failed": "Failed to create backup",
        "backup_file_missing": "Source file not found",
        "backup_file_not_found": "Backup file not found",
        "restore_success": "File successfully restored",
        "restore_failed": "Restore failed",
        "translation_file_missing": "Translation file missing: {file}",
        "translation_mismatch": "Incorrect number of translations: {provided} provided, {expected} expected",
        "translations_missing": "Missing translations: {missing_count} (expected: {expected}, found: {found})",
        "translations_extra": "Extra translations: {extra_count} (expected: {expected}, found: {found})",
        "validation_correspondence_error": "Validation error: {error}",
        "main_file_missing": "Main file missing: {file}",
        "asterix_file_missing": "Asterisk file missing: {file}",
        "empty_file_missing": "Empty text file missing: {file}",
        "temp_folder_missing": "Temporary folder does not exist: {folder}",
        "folder_creation_failed": "Failed to create folder: {error}",
        "no_game_found": "No project detected",
        "start_extraction_suggestion": "Start by extracting an .rpy file",
        "fix_structure_errors": "Fix structure errors before proceeding",
        "cleanup_old_files": "Consider cleaning up old temporary files",
        "backup_folder_not_found": "Backup folder not found: {folder}",
        "quote_correction_applied": "Quote correction applied: {count} corrections",
        "quote_correction_error": "Error during quote correction: {error}",
        "game_structure_validation": "Game structure validation",
        "folders_created": "Folders created successfully",
        "folders_missing": "Missing folders detected",
        "insufficient_write_permissions": "Insufficient write permissions: {folder}",
        "extraction_files_validation": "Extraction files validation",
        "required_files_missing": "Required files missing for {file_base}",
        "cleanup_completed": "Cleanup completed: {files_removed} removed, {files_kept} kept",
        "cleanup_failed": "Error during cleanup: {error}",
        "diagnostic_complete": "Diagnostic complete",
        "diagnostic_error": "Error during diagnostic: {error}",
        "application_state_healthy": "Application state healthy",
        "application_issues_detected": "Issues detected in application"
    }
}