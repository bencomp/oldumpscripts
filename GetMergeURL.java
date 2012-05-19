import java.sql.*;
import java.io.*;
import java.util.*;

public class GetMergeURL
{
    private Connection con;
    
    public GetMergeURL()
    {
        try
        {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            con = DriverManager.getConnection("jdbc:mysql://localhost/openlibrary", "olbot", "public");
            String q = "SELECT slug, dobslug, dodslug FROM dupe_authors_dates ORDER BY number DESC";
            PreparedStatement p = con.prepareStatement(q);
            ResultSet rs = p.executeQuery();
            
            PreparedStatement p2 = con.prepareStatement("SELECT `key` FROM authors_2012_04_dates WHERE slug = ? AND dobslug = ? AND dodslug = ? ORDER BY 1 ASC");
            PreparedStatement p2n1 = con.prepareStatement("SELECT `key` FROM authors_2012_04_dates WHERE slug = ? AND dobslug IS NULL AND dodslug = ? ORDER BY 1 ASC");
            PreparedStatement p2n2 = con.prepareStatement("SELECT `key` FROM authors_2012_04_dates WHERE slug = ? AND dobslug = ? AND dodslug IS NULL ORDER BY 1 ASC");
            PreparedStatement p2nn = con.prepareStatement("SELECT `key` FROM authors_2012_04_dates WHERE slug = ? AND dobslug IS NULL AND dodslug IS NULL ORDER BY 1 ASC");
            ResultSet rs2 = null;
            String url = null;
            int fileNum = 1;
            List<String> listOfUrls = new LinkedList<String>();
            
            while(rs.next())
            {
                String slug = rs.getString("slug");
                String dobslug = rs.getString("dobslug");
                String dodslug = rs.getString("dodslug");
                
                if (dobslug == null && dodslug == null)
                {
                    p2nn.setString(1, slug);
                    rs2 = p2nn.executeQuery();
                }
                else if (dobslug == null)
                {
                    p2n1.setString(1, slug);
                    p2n1.setString(2, dodslug);
                    rs2 = p2n1.executeQuery();
                }
                else if (dodslug == null)
                {
                    p2n2.setString(1, slug);
                    p2n2.setString(2, dobslug);
                    rs2 = p2n2.executeQuery();
                }
                else
                {
                    p2.setString(1, slug);
                    p2.setString(2, dobslug);
                    p2.setString(3, dodslug);
                    rs2 = p2.executeQuery();
                }
                
                url = createURL(rs2);
                listOfUrls.add(wrapURL(url, slug+" | "+dobslug+" | "+dodslug));
                
                // Limit to 100 URLs per file
                if (rs.getRow() % 100 == 0)
                {
                    writeFile(fileNum, listOfUrls);
                    System.out.println("Wrote file number "+fileNum);
                    fileNum++;
                    listOfUrls.clear();
                }
                
            }
            
            if (!listOfUrls.isEmpty())
            {
                writeFile(fileNum, listOfUrls);
                System.out.println("Wrote file number "+fileNum);
            }
            
            con.close();
        }
        catch (SQLException e)
        {
            System.out.println("SQL exception in main: " + e.getMessage());
        }
        catch (Exception e)
        {
            System.out.println("General exception in main: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private String createURL(ResultSet rs) throws SQLException
    {
        String s = "http://openlibrary.org/authors/merge?";
        while (rs.next())
        {
            s += "key=" + rs.getString(1) + "&";
        }
        //System.out.println(s);
        return s;
    }
    
    private String wrapURL(String url, String label)
    {
        return "<a href=\""+url+"\" target=\"_blank\">"+label+"</a>";
    }
    
    private void writeFile(int fileNum, List<String> listOfUrls)
    {
        try
        {
            BufferedWriter fw = new BufferedWriter( new FileWriter("ol_merge_links_"+fileNum+".html"));
            fw.write("<html>");
            fw.newLine();
            fw.write("<head>");
            fw.newLine();
            fw.write("<title>Merge Authors</title>");
            fw.newLine();
            fw.write("</head>");
            fw.newLine();
            fw.write("<body>");
            fw.newLine();
            fw.write("<p>Take care when merging, it's easier to merge than to split authors :)</p>");
            fw.newLine();
            
            Iterator<String> it = listOfUrls.iterator();
            while (it.hasNext())
            {
                fw.write( it.next() + "<br />" );
                fw.newLine();
            }
            fw.write( "<p>Next file: <a href=\"ol_merge_links_"+(fileNum+1)+".html\">"+(fileNum+1)+"</a></p></body></html>");
            fw.close();
        }
        catch (IOException ie)
        {
            System.out.println("IO exception: " + ie.getMessage());
        }
        catch (Exception se)
        {
            System.out.println("General exception in writeFile: " + se.getMessage());
        }
    }
    
    public static void main(String[] args)
    {
        new GetMergeURL();
    }
}