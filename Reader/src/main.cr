require "json"

def main
    name = ARGV[0]
    chapter = ARGV[1]?
    create_file name, chapter
end

def create_file(name, chapter)
    json, min_chapter = generate_map name
    if chapter.nil?
        chapter = min_chapter
    end
    string = File.read("/home/justinas/Coding Stuff/Crystal Stuff/manga-reader/Reader/HTML Boilerplate/index.html")
        .sub("title_placeholder", name)
        .sub("current_chapter_placeholder", chapter)
        .sub("json_placeholder", json.to_json)
    File.write("/home/justinas/Coding Stuff/Crystal Stuff/manga-reader/Reader/HTML/index.html", string)
    `xdg-open "/home/justinas/Coding Stuff/Crystal Stuff/manga-reader/Reader/HTML/index.html"`
end

def generate_map(manga_name)
    output = Array(Array(String)).new
    dirs = Dir["/home/justinas/.manga/#{manga_name}/*"].sort do |a, b|
        a.split('/')[-1].to_f <=> b.split('/')[-1].to_f
    end
    chapter = dirs[0].split('/')[-1]
    dirs.each do |i|
        new_dirs = Dir["#{i}/*"]
        new_dirs = new_dirs.sort do |a, b|
            a.split('/')[-1].split('.')[0].to_i <=> b.split('/')[-1].split('.')[0].to_i
        end
        output << new_dirs.insert(0, i.split('/')[-1])
    end
    {output, chapter}
end


main
