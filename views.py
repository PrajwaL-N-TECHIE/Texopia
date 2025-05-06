from django.http import HttpResponse
from django.shortcuts import render
import re

def index(request):
    return render(request, 'index.html')

def analyze(request):
    if request.method == 'POST':
        djtext = request.POST.get('text', '')
        removepunc = request.POST.get('removepunc', 'off')
        fullcaps = request.POST.get('fullcaps', 'off')
        newlineremove = request.POST.get('newlineremove', 'off')
        spaceremove = request.POST.get('spaceremove', 'off')
        reverse_text = request.POST.get('reverseText', 'off')
        remove_duplicates = request.POST.get('removeDuplicates', 'off')
        find_text = request.POST.get('findText', '')
        replace_text = request.POST.get('replaceText', '')
        charcount = request.POST.get('charcount', 'off')
        wordcount = request.POST.get('wordcount', 'off')

        analyzed = djtext
        purposes = []

        # Punctuation Removal
        if removepunc == 'on':
            punctuations = '''.,!?;:'"-—()[]{}.../\|@#$%&*^~_'''
            analyzed = ''.join(char for char in analyzed if char not in punctuations)
            purposes.append('Removed Punctuations')

        # Uppercase Conversion
        if fullcaps == 'on':
            analyzed = analyzed.upper()
            purposes.append('Converted to UPPERCASE')

        # Newline Removal
        if newlineremove == 'on':
            analyzed = analyzed.replace('\n', '').replace('\r', '')
            purposes.append('Removed New Lines')

        # Extra Space Removal
        if spaceremove == 'on':
            analyzed = ' '.join(analyzed.split())
            purposes.append('Removed Extra Spaces')

        # Reverse Text
        if reverse_text == 'on':
            analyzed = analyzed[::-1]
            purposes.append('Reversed Text')

        # Remove Duplicate Lines
        if remove_duplicates == 'on':
            lines = analyzed.split('\n')
            unique_lines = []
            seen_lines = set()
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and stripped_line not in seen_lines:
                    seen_lines.add(stripped_line)
                    unique_lines.append(line)
            analyzed = '\n'.join(unique_lines)
            purposes.append('Removed Duplicate Lines')

        # Find and Replace
        if find_text:
            analyzed = analyzed.replace(find_text, replace_text)
            purposes.append(f'Replaced "{find_text}" with "{replace_text}"')

        # Character Count
        if charcount == 'on':
            purposes.append(f'Character Count: {len(analyzed)}')

        # Word Count
        if wordcount == 'on':
            purposes.append(f'Word Count: {len(re.findall(r"\\w+", analyzed))}')

        # If no operation was selected
        if not purposes:
            purposes.append('No Operation Selected')

        params = {
            'purpose_list': purposes,
            'analyzed_text': analyzed,
            'char_count': len(analyzed),
            'word_count': len(re.findall(r'\w+', analyzed)),
        }

        return render(request, 'analyze.html', params)

    return HttpResponse("Invalid request method")
