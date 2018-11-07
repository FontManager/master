/* FontManager.vapi generated by vapigen-0.42, do not modify. */

[CCode (cprefix = "FontManager", gir_namespace = "FontManager", gir_version = "0.7.4", lower_case_cprefix = "font_manager_")]
namespace FontManager {
	[CCode (cheader_filename = "font-manager-alias.h", type_id = "font_manager_alias_element_get_type ()")]
	public class AliasElement : GLib.Object {
		[CCode (has_construct_function = false)]
		public AliasElement (string? family);
		public unowned FontManager.StringHashset @get (string priority);
		[NoAccessorMethod]
		public FontManager.StringHashset accept { owned get; set; }
		[NoAccessorMethod]
		public FontManager.StringHashset @default { owned get; set; }
		[NoAccessorMethod]
		public string family { owned get; set; }
		[NoAccessorMethod]
		public FontManager.StringHashset prefer { owned get; set; }
	}
	[CCode (cheader_filename = "font-manager-aliases.h", type_id = "font_manager_aliases_get_type ()")]
	public class Aliases : GLib.Object {
		[CCode (has_construct_function = false)]
		public Aliases ();
		public bool add (string family);
		public bool add_element (owned FontManager.AliasElement element);
		public bool contains (string family);
		public unowned FontManager.AliasElement @get (string family);
		public string? get_filepath ();
		public GLib.List<weak FontManager.AliasElement> list ();
		public bool load ();
		public bool remove (string family);
		public bool save ();
		[NoAccessorMethod]
		public string config_dir { owned get; set; }
		[NoAccessorMethod]
		public string target_file { owned get; set; }
	}
	[CCode (cheader_filename = "font-manager-codepoint-list.h", type_id = "font_manager_codepoint_list_get_type ()")]
	public class CodepointList : GLib.Object, Unicode.CodepointList {
		[CCode (has_construct_function = false)]
		public CodepointList ();
		public void set_filter (GLib.List<uint>? filter);
		public void set_font (Json.Object? font);
		public GLib.List<uint> filter { set; }
		public Json.Object font { set; }
	}
	[CCode (cheader_filename = "font-manager-database.h", type_id = "font_manager_database_get_type ()")]
	public class Database : GLib.Object {
		public Sqlite.Database db;
		public Sqlite.Statement stmt;
		[CCode (has_construct_function = false)]
		public Database ();
		public void attach (FontManager.DatabaseType type) throws FontManager.DatabaseError;
		public void begin_transaction () throws FontManager.DatabaseError;
		public void commit_transaction () throws FontManager.DatabaseError;
		public void detach (FontManager.DatabaseType type) throws FontManager.DatabaseError;
		public static GLib.Quark error_quark ();
		public void execute_query (string sql) throws FontManager.DatabaseError;
		public static string? get_file (FontManager.DatabaseType type);
		public Json.Object? get_object (string sql) throws FontManager.DatabaseError;
		public static unowned string get_type_name (FontManager.DatabaseType type);
		public int get_version () throws FontManager.DatabaseError;
		public void initialize (FontManager.DatabaseType type) throws FontManager.DatabaseError;
		public FontManager.DatabaseIterator iterator ();
		public void open () throws FontManager.DatabaseError;
		public void set_version (int version) throws FontManager.DatabaseError;
		public void vacuum () throws FontManager.DatabaseError;
		[NoAccessorMethod]
		public string? file { owned get; set; }
	}
	[CCode (cheader_filename = "font-manager-database.h", type_id = "font_manager_database_iterator_get_type ()")]
	public class DatabaseIterator : GLib.Object {
		[CCode (has_construct_function = false)]
		public DatabaseIterator (FontManager.Database db);
		public unowned Sqlite.Statement @get ();
		public bool next ();
	}
	[CCode (cheader_filename = "font-manager-family.h", type_id = "font_manager_family_get_type ()")]
	public class Family : GLib.Object, FontManager.JsonProxy {
		[CCode (has_construct_function = false)]
		public Family ();
		public unowned Json.Object get_default_variant ();
		[NoAccessorMethod]
		public string description { owned get; }
		[NoAccessorMethod]
		public string family { owned get; }
		[NoAccessorMethod]
		public int n_variations { get; }
		[NoAccessorMethod]
		public Json.Array variations { owned get; }
	}
	[CCode (cheader_filename = "font-manager-font.h", type_id = "font_manager_font_get_type ()")]
	public class Font : GLib.Object, FontManager.JsonProxy {
		[CCode (has_construct_function = false)]
		public Font ();
		[NoAccessorMethod]
		public string description { owned get; }
		[NoAccessorMethod]
		public string family { owned get; }
		[NoAccessorMethod]
		public string filepath { owned get; }
		[NoAccessorMethod]
		public int findex { get; }
		[NoAccessorMethod]
		public int slant { get; }
		[NoAccessorMethod]
		public int spacing { get; }
		[NoAccessorMethod]
		public string style { owned get; }
		[NoAccessorMethod]
		public int weight { get; }
		[NoAccessorMethod]
		public int width { get; }
	}
	[CCode (cheader_filename = "font-manager-font-info.h", type_id = "font_manager_font_info_get_type ()")]
	public class FontInfo : GLib.Object, FontManager.JsonProxy {
		[CCode (has_construct_function = false)]
		public FontInfo ();
		[NoAccessorMethod]
		public string checksum { owned get; }
		[NoAccessorMethod]
		public string? copyright { owned get; }
		[NoAccessorMethod]
		public string? description { owned get; }
		[NoAccessorMethod]
		public string? designer { owned get; }
		[NoAccessorMethod]
		public string? designer_url { owned get; }
		[NoAccessorMethod]
		public string family { owned get; }
		[NoAccessorMethod]
		public string filepath { owned get; }
		[NoAccessorMethod]
		public string filesize { owned get; }
		[NoAccessorMethod]
		public string filetype { owned get; }
		[NoAccessorMethod]
		public int findex { get; }
		[NoAccessorMethod]
		public int fsType { get; }
		[NoAccessorMethod]
		public string? license_data { owned get; }
		[NoAccessorMethod]
		public string license_type { owned get; }
		[NoAccessorMethod]
		public string? license_url { owned get; }
		[NoAccessorMethod]
		public int n_glyphs { get; }
		[NoAccessorMethod]
		public int owner { get; }
		[NoAccessorMethod]
		public Json.Array panose { owned get; }
		[NoAccessorMethod]
		public string psname { owned get; }
		[NoAccessorMethod]
		public string style { owned get; }
		[NoAccessorMethod]
		public string vendor { owned get; }
		[NoAccessorMethod]
		public string version { owned get; }
	}
	[CCode (cheader_filename = "font-manager-font-model.h", type_id = "font_manager_font_model_get_type ()")]
	public class FontModel : GLib.Object, Gtk.TreeDragDest, Gtk.TreeDragSource, Gtk.TreeModel {
		[CCode (has_construct_function = false)]
		public FontModel ();
		[NoAccessorMethod]
		public Json.Array source_array { owned get; set; }
	}
	[CCode (cheader_filename = "font-manager-properties.h", type_id = "font_manager_properties_get_type ()")]
	public class Properties : GLib.Object {
		[CCode (has_construct_function = false)]
		public Properties ();
		[NoWrapper]
		public virtual void add_match_criteria (FontManager.XmlWriter writer);
		public bool discard ();
		public string? get_filepath ();
		public virtual bool load ();
		[NoWrapper]
		public virtual void parse_edit_node (Xml.Node edit_node);
		[NoWrapper]
		public virtual void parse_test_node (Xml.Node test_node);
		public void reset ();
		public virtual bool save ();
		[NoAccessorMethod]
		public bool antialias { get; set; }
		[NoAccessorMethod]
		public bool autohint { get; set; }
		[NoAccessorMethod]
		public string config_dir { owned get; set; }
		[NoAccessorMethod]
		public double dpi { get; set; }
		[NoAccessorMethod]
		public bool embeddedbitmap { get; set; }
		[NoAccessorMethod]
		public bool hinting { get; set; }
		[NoAccessorMethod]
		public int hintstyle { get; set; }
		[NoAccessorMethod]
		public int lcdfilter { get; set; }
		[NoAccessorMethod]
		public double less { get; set; }
		[NoAccessorMethod]
		public double more { get; set; }
		[NoAccessorMethod]
		public int rgba { get; set; }
		[NoAccessorMethod]
		public double scale { get; set; }
		[NoAccessorMethod]
		public string target_file { owned get; set; }
		[NoAccessorMethod]
		public int type { get; set; }
	}
	[CCode (cheader_filename = "font-manager-selections.h", type_id = "font_manager_selections_get_type ()")]
	public class Selections : FontManager.StringHashset {
		[CCode (has_construct_function = false)]
		public Selections ();
		public string? get_filepath ();
		[NoWrapper]
		public virtual unowned Xml.Node? get_selections (Xml.Doc* doc);
		public virtual bool load ();
		[NoWrapper]
		public virtual void parse_selections (Xml.Node selections);
		public virtual bool save ();
		[NoWrapper]
		public virtual void write_selections (FontManager.XmlWriter writer);
		[NoAccessorMethod]
		public string config_dir { owned get; set; }
		[NoAccessorMethod]
		public string target_element { owned get; set; }
		[NoAccessorMethod]
		public string target_file { owned get; set; }
		public virtual signal void changed ();
	}
	[CCode (cheader_filename = "font-manager-source.h", type_id = "font_manager_source_get_type ()")]
	public class Source : GLib.Object {
		[CCode (has_construct_function = false)]
		public Source (GLib.File file);
		public string? get_status_message ();
		public void update ();
		[NoAccessorMethod]
		public bool active { get; set; }
		[NoAccessorMethod]
		public bool available { get; }
		[NoAccessorMethod]
		public GLib.File file { owned get; set; }
		[NoAccessorMethod]
		public string icon_name { owned get; }
		[NoAccessorMethod]
		public string name { owned get; }
		[NoAccessorMethod]
		public string path { owned get; }
	}
	[CCode (cheader_filename = "string-hashset.h", cname = "StringHashset", type_id = "string_hashset_get_type ()")]
	public class StringHashset : GLib.Object {
		[CCode (cname = "string_hashset_new", has_construct_function = false)]
		public StringHashset ();
		[CCode (cname = "string_hashset_add")]
		public bool add (string str);
		[CCode (cname = "string_hashset_add_all")]
		public bool add_all (GLib.List<string> add);
		[CCode (cname = "string_hashset_clear")]
		public void clear ();
		[CCode (cname = "string_hashset_contains")]
		public bool contains (string str);
		[CCode (cname = "string_hashset_contains_all")]
		public bool contains_all (GLib.List<string> contents);
		[CCode (cname = "string_hashset_get")]
		public unowned string @get (uint index);
		[CCode (cname = "string_hashset_list")]
		public GLib.List<weak string> list ();
		[CCode (cname = "string_hashset_remove")]
		public bool remove (string str);
		[CCode (cname = "string_hashset_remove_all")]
		public bool remove_all (GLib.List<string> remove);
		[CCode (cname = "string_hashset_retain_all")]
		public bool retain_all (GLib.List<string> retain);
		[NoAccessorMethod]
		public uint size { get; }
	}
	[CCode (cheader_filename = "font-manager-xml-writer.h", type_id = "font_manager_xml_writer_get_type ()")]
	public class XmlWriter : GLib.Object {
		[CCode (has_construct_function = false)]
		public XmlWriter ();
		public void add_assignment (string a_name, string a_type, string a_val);
		public void add_elements (string e_type, GLib.List<string> elements);
		public void add_patelt (string p_name, string p_type, string p_val);
		public void add_selections (string selection_type, GLib.List<string> selections);
		public void add_test_element (string t_name, string t_test, string t_type, string t_val);
		public bool close ();
		public void discard ();
		public int end_element ();
		public bool open (string filepath);
		public int start_element (string name);
		public int write_attribute (string name, string content);
		public int write_element (string name, string content);
		[NoAccessorMethod]
		public string filepath { owned get; }
	}
	[CCode (cheader_filename = "font-manager-filter.h", type_cname = "FontManagerFilterInterface", type_id = "font_manager_filter_get_type ()")]
	public interface Filter : GLib.Object {
		public abstract void update ();
		public abstract bool visible_func (Gtk.TreeModel model, Gtk.TreeIter iter);
		[NoAccessorMethod]
		public abstract string comment { owned get; set; }
		[NoAccessorMethod]
		public abstract string icon { owned get; set; }
		[NoAccessorMethod]
		public abstract int index { get; set; }
		[NoAccessorMethod]
		public abstract string name { owned get; set; }
		[NoAccessorMethod]
		public abstract int size { get; }
	}
	[CCode (cheader_filename = "font-manager-json-proxy.h", type_cname = "FontManagerJsonProxyInterface", type_id = "font_manager_json_proxy_get_type ()")]
	public interface JsonProxy : GLib.Object {
		[NoAccessorMethod]
		public abstract Json.Object source_object { owned get; set; }
	}
	[CCode (cheader_filename = "font-manager-orthography.h", cname = "OrthographyData", has_type_id = false)]
	public struct OrthographyData {
		public weak string name;
		public weak string native;
		public unichar key;
		public weak string sample;
		[CCode (array_length = false)]
		public weak string pangram[10];
		[CCode (array_length = false)]
		public weak unichar values[4096];
	}
	[CCode (cheader_filename = "utils.h", cname = "ProgressData", has_type_id = false)]
	public struct ProgressData {
		public uint processed;
		public uint total;
		public weak string message;
	}
	[CCode (cheader_filename = "font-manager-database.h", cprefix = "FONT_MANAGER_DATABASE_TYPE_", has_type_id = false)]
	public enum DatabaseType {
		BASE,
		FONT,
		METADATA,
		ORTHOGRAPHY
	}
	[CCode (cheader_filename = "font-manager-font-model.h", cprefix = "FONT_MANAGER_FONT_MODEL_", has_type_id = false)]
	public enum FontModelColumn {
		OBJECT,
		NAME,
		DESCRIPTION,
		COUNT,
		N_COLUMNS
	}
	[CCode (cheader_filename = "font-manager-properties.h", cprefix = "FONT_MANAGER_PROPERTIES_TYPE_", has_type_id = false)]
	public enum PropertiesType {
		DEFAULT,
		DISPLAY
	}
	[CCode (cheader_filename = "font-manager-database.h", cprefix = "FONT_MANAGER_DATABASE_ERROR_")]
	public errordomain DatabaseError {
		OK,
		ERROR,
		INTERNAL,
		PERM,
		ABORT,
		BUSY,
		LOCKED,
		NOMEM,
		READONLY,
		INTERRUPT,
		IOERR,
		CORRUPT,
		NOTFOUND,
		FULL,
		CANTOPEN,
		PROTOCOL,
		EMPTY,
		SCHEMA,
		TOOBIG,
		CONSTRAINT,
		MISMATCH,
		MISUSE,
		NOLFS,
		AUTH,
		FORMAT,
		RANGE,
		NOTADB,
		NOTICE,
		WARNING,
		ROW,
		DONE
	}
	[CCode (cheader_filename = "utils.h", has_target = false)]
	public delegate bool ProgressCallback (FontManager.ProgressData data);
	[CCode (cheader_filename = "font-manager-database.h", cname = "FONT_MANAGER_CURRENT_DATABASE_VERSION")]
	public const int CURRENT_DATABASE_VERSION;
	[CCode (cheader_filename = "font-manager-orthography.h", cname = "END_OF_DATA")]
	public const int END_OF_DATA;
	[CCode (cheader_filename = "font-manager-orthography.h", cname = "START_RANGE_PAIR")]
	public const int START_RANGE_PAIR;
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "add_application_font")]
	public static bool add_application_font (string filepath);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "add_application_font_directory")]
	public static bool add_application_font_directory (string dir);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "clear_application_fonts")]
	public static void clear_application_fonts ();
	[CCode (cheader_filename = "json.h", cname = "compare_json_font_node")]
	public static int compare_json_font_node (Json.Node node_a, Json.Node node_b);
	[CCode (cheader_filename = "json.h", cname = "compare_json_int_member")]
	public static int compare_json_int_member (string member_name, Json.Object a, Json.Object b);
	[CCode (cheader_filename = "json.h", cname = "compare_json_string_member")]
	public static int compare_json_string_member (string member_name, Json.Object a, Json.Object b);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "enable_user_font_configuration")]
	public static bool enable_user_font_configuration (bool enable);
	[CCode (cheader_filename = "utils.h", cname = "exists")]
	public static bool exists (string filepath);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_attributes_from_filepath")]
	public static Json.Object get_attributes_from_filepath (string filepath, int index);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_available_fonts")]
	public static Json.Object get_available_fonts (string? family_name);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_available_fonts_for_chars")]
	public static Json.Object get_available_fonts_for_chars (string chars);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_available_fonts_for_lang")]
	public static Json.Object get_available_fonts_for_lang (string lang_id);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_charset_from_filepath")]
	public static GLib.List<weak unichar>? get_charset_from_filepath (string filepath, int index);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "get_charset_from_font_object")]
	public static GLib.List<weak unichar>? get_charset_from_font_object (Json.Object font_object);
	[CCode (cheader_filename = "font-manager-database.h")]
	public static FontManager.Database get_database (FontManager.DatabaseType type) throws FontManager.DatabaseError;
	[CCode (cheader_filename = "font-manager-freetype.h")]
	public static long get_face_count (string filepath);
	[CCode (cheader_filename = "utils.h", cname = "get_file_extension")]
	public static string? get_file_extension (string filepath);
	[CCode (cheader_filename = "utils.h", cname = "get_file_owner")]
	public static int get_file_owner (string filepath);
	[CCode (cheader_filename = "utils.h", cname = "get_gsettings")]
	public static GLib.Settings? get_gsettings (string schema_id);
	[CCode (cheader_filename = "utils.h", cname = "get_local_time")]
	public static string? get_local_time ();
	[CCode (cheader_filename = "font-manager-database.h")]
	public static void get_matching_families_and_fonts (FontManager.Database db, FontManager.StringHashset families, FontManager.StringHashset fonts, string sql) throws FontManager.DatabaseError;
	[CCode (cheader_filename = "font-manager-freetype.h")]
	public static Json.Object get_metadata (string filepath, int index);
	[CCode (cheader_filename = "font-manager-orthography.h")]
	public static Json.Object? get_orthography_results (Json.Object? font);
	[CCode (cheader_filename = "utils.h", cname = "get_package_cache_directory")]
	public static string? get_package_cache_directory ();
	[CCode (cheader_filename = "utils.h", cname = "get_package_config_directory")]
	public static string? get_package_config_directory ();
	[CCode (cheader_filename = "font-manager-orthography.h")]
	public static string? get_sample_string_for_orthography (Json.Object orthography, GLib.List<uint>? charset);
	[CCode (cheader_filename = "utils.h", cname = "get_user_font_directory")]
	public static string? get_user_font_directory ();
	[CCode (cheader_filename = "utils.h", cname = "get_user_fontconfig_directory")]
	public static string? get_user_fontconfig_directory ();
	[CCode (cheader_filename = "utils.h", cname = "is_dir")]
	public static bool is_dir (string filepath);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "list_available_font_families")]
	public static GLib.List<string>? list_available_font_families ();
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "list_available_font_files")]
	public static GLib.List<string>? list_available_font_files ();
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "list_font_directories")]
	public static GLib.List<string>? list_font_directories (bool recursive);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "list_user_font_directories")]
	public static GLib.List<string>? list_user_font_directories ();
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "load_font_configuration_file")]
	public static bool load_font_configuration_file (string filepath);
	[CCode (cheader_filename = "json.h", cname = "load_json_file")]
	public static Json.Node? load_json_file (string filepath);
	[CCode (cheader_filename = "utils.h", cname = "natural_sort")]
	public static int natural_sort (string s1, string s2);
	[CCode (cheader_filename = "json.h", cname = "print_json_array")]
	public static string print_json_array (Json.Array json_arr, bool pretty);
	[CCode (cheader_filename = "json.h", cname = "print_json_object")]
	public static string print_json_object (Json.Object json_obj, bool pretty);
	[CCode (cheader_filename = "json.h", cname = "set_json_error")]
	public static void set_json_error (Json.Object json_obj, int err_code, string err_msg);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "sort_json_font_listing")]
	public static Json.Array sort_json_font_listing (Json.Object json_obj);
	[CCode (cheader_filename = "json.h", cname = "str_list_to_json_array")]
	public static Json.Array str_list_to_json_array (GLib.List<string> slist);
	[CCode (cheader_filename = "font-manager-database.h")]
	public static async bool sync_database (FontManager.Database db, FontManager.DatabaseType type, FontManager.ProgressCallback? progress, GLib.Cancellable? cancellable) throws FontManager.DatabaseError, GLib.Error;
	[CCode (cheader_filename = "utils.h", cname = "to_filename")]
	public static string? to_filename (string str);
	[CCode (cheader_filename = "font-manager-fontconfig.h", cname = "update_font_configuration")]
	public static bool update_font_configuration ();
	[CCode (cheader_filename = "json.h", cname = "write_json_file")]
	public static bool write_json_file (Json.Node root, string filepath);
}
