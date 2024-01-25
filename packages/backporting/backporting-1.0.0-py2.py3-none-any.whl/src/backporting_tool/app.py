import os

from src.backporting_tool.google_diff_match_patch import diff_match_patch


class BackPortingSystem:
    @staticmethod
    def check_file_exists(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def apply_patch(original_text, patch_text):
        dmp = diff_match_patch()
        patches = dmp.patch_fromText(patch_text)
        result_text, _ = dmp.patch_apply(patches, original_text)
        return result_text

    @staticmethod
    def create_patch(text1, text2):
        dmp = diff_match_patch()
        diffs = dmp.diff_main(text1, text2)
        patch = dmp.patch_make(text1, diffs)
        patch_text = dmp.patch_toText(patch)
        return patch_text

    @staticmethod
    def apply_patch_with_conflict_handling(original_text, patch_text):
        dmp = diff_match_patch()
        patches = dmp.patch_fromText(patch_text)
        result_text, results = dmp.patch_apply(patches, original_text)

        conflicts = []
        for i, result in enumerate(results):
            if not result:
                patch = patches[i]
                start_pos = patch.start1
                end_pos = start_pos + sum([len(diff[1]) for diff in patch.diffs if diff[0] != 1])
                conflict_text = original_text[start_pos:end_pos]
                conflicts.append((start_pos, end_pos, conflict_text))

        if conflicts:
            for start, end, text in conflicts:
                print(f"Conflict detected at positions {start} to {end}: '{text}'")
                print("1. Keep original text")
                print("2. Use patched text")
                print("3. Enter custom resolution")
                choice = input("Choose an option (1, 2, or 3): ")
                if choice == '1':
                    continue
                elif choice == '2':
                    patch_text = ''.join([diff[1] for diff in patch.diffs])
                    result_text = result_text[:start] + patch_text + result_text[end:]
                elif choice == '3':
                    custom_text = input("Enter custom resolution text: ")
                    result_text = result_text[:start] + custom_text + result_text[end:]
                else:
                    print("Invalid choice. Keeping original text.")
            return result_text
        else:
            return result_text


def main():
    original_file_path = input("Enter the original file path: ")
    modified_file_path = input("Enter the modified file path: ")
    target_file_path = input("Enter the target file path: ")

    for i, file_path in enumerate([original_file_path, modified_file_path, target_file_path], start=1):
        if not BackPortingSystem.check_file_exists(file_path):
            print(f"File {i} does not exist: {file_path}")
            exit(1)

    with open(original_file_path, 'r') as file:
        original_text = file.read()

    with open(modified_file_path, 'r') as file:
        modified_text = file.read()

    with open(target_file_path, 'r') as file:
        target_text = file.read()

    patch_text = BackPortingSystem.create_patch(original_text, modified_text)

    result = BackPortingSystem.apply_patch_with_conflict_handling(target_text, patch_text)
    open(target_file_path, 'w').close()
    with open(target_file_path, 'w') as writer:
        writer.write(result)

    print("Changes are successfully applied.")


if __name__ == "__main__":
    main()
