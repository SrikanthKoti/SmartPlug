package com.example.smartplug;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {
    public static ImageButton imgb;
    public static TextView t1;
    TextToSpeech speak;
    int result;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FloatingActionButton fab = findViewById(R.id.fab);
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();
        navigationView.setNavigationItemSelectedListener(this);
        imgb = (ImageButton) findViewById(R.id.imageButton6);
        t1=(TextView)findViewById(R.id.t1);

        speak = new TextToSpeech(MainActivity.this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status == TextToSpeech.SUCCESS)
                {
                    result = speak.setLanguage(Locale.ENGLISH);
                    if(result == TextToSpeech.LANG_NOT_SUPPORTED || result == TextToSpeech.LANG_MISSING_DATA)
                    {
                        Toast.makeText(getApplicationContext(),"language unsupported",Toast.LENGTH_LONG).show();
                    }
                }
                else {
                    Toast.makeText(getApplicationContext(),"not supporting",Toast.LENGTH_LONG).show();
                }
            }
        });
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_home) {
            // Handle the camera action
        } else if (id == R.id.nav_status) {

            Intent i1=new Intent(this,graph_.class);
            startActivity(i1);


        } else if (id == R.id.nav_statistics) {

        } else if (id == R.id.nav_schedule) {
            Intent i1=new Intent(this,schedule.class);
            startActivity(i1);


        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    public void doOnOff(View view) throws IOException, URISyntaxException {

        //for ch
        DownloadWebPageTask task = new DownloadWebPageTask();
        task.execute("http://sriki007.pythonanywhere.com/getonoffvalue");

        WebView myWebView = (WebView) findViewById(R.id.good);
        myWebView.loadUrl("http://sriki007.pythonanywhere.com/setonoff");
    }

    public void speak_to_assistant(View view) {

        Intent i1=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i1.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        i1.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.ENGLISH);

        if(i1.resolveActivity(getPackageManager())!=null)
        {
            startActivityForResult(i1,10);
        }
        else
        {
            Toast.makeText(this,"YOUR PHONE NOT SUPPORTED",Toast.LENGTH_SHORT).show();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode)
        {
            case 10:
                if(data!=null)
                {
                    ArrayList<String> result=data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                        System.out.println(result.get(0));
                        String voice=result.get(0);
                        if(voice.equals("hey") || voice.equals("hello") || voice.equals("hey friday") || voice.equals("hello friday") || voice.equals("friday"))
                        {
                            speak.speak("hello sir",TextToSpeech.QUEUE_FLUSH,null);
                        }
                        else if(voice.equals("check device status") || voice.equals("device status"))
                        {
                            speak.speak("checking",TextToSpeech.QUEUE_FLUSH,null);
                            System.out.println(1);
                            download_for_speak download_for_speakx = new download_for_speak();
                            System.out.println(2);
                            download_for_speakx.execute("http://sriki007.pythonanywhere.com/getonoffvalue");

                            String find=download_for_speakx.returnonoff();
                            System.out.println(1);
                            speak.speak("your device was "+find+" now",TextToSpeech.QUEUE_FLUSH,null);
                        }
                        else if(voice.equals("on device") || voice.equals("device on"))
                        {
                            download_for_speak download_for_speakx = new download_for_speak();
                            download_for_speakx.execute("http://sriki007.pythonanywhere.com/getonoffvalue");
                            String find=download_for_speakx.returnonoff();
                            if(find.equals("on"))
                            {
                                speak.speak("your device was already on",TextToSpeech.QUEUE_FLUSH,null);
                            }
                            else
                            {
                                WebView myWebView = (WebView) findViewById(R.id.good);
                                myWebView.loadUrl("http://sriki007.pythonanywhere.com/setonoff");
                                speak.speak("your device was on now",TextToSpeech.QUEUE_FLUSH,null);
                            }
                        }
                        else if(voice.equals("of device") || voice.equals("device of") || voice.equals("off device") || voice.equals("device off"))
                        {
                            download_for_speak download_for_speakx = new download_for_speak();
                            download_for_speakx.execute("http://sriki007.pythonanywhere.com/getonoffvalue");
                            String find=download_for_speakx.returnonoff();
                            if(find.equals("off"))
                            {
                                speak.speak("your device was already off",TextToSpeech.QUEUE_FLUSH,null);
                            }
                            else
                            {
                                WebView myWebView = (WebView) findViewById(R.id.good);
                                myWebView.loadUrl("http://sriki007.pythonanywhere.com/setonoff");
                                speak.speak("your device was off now",TextToSpeech.QUEUE_FLUSH,null);
                            }
                        }

                }
                break;
        }
    }
}

class download_for_speak extends AsyncTask<String, Void, String> {
     public String data;
    @Override
    protected String doInBackground(String... urls) {
        String response = "";
        for (String url : urls) {
            DefaultHttpClient client = new DefaultHttpClient();
            HttpGet httpGet = new HttpGet(url);
            try {
                HttpResponse execute = client.execute(httpGet);
                InputStream content = execute.getEntity().getContent();

                BufferedReader buffer = new BufferedReader(
                        new InputStreamReader(content));
                String s = "";
                while ((s = buffer.readLine()) != null) {
                    response += s;
                }

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return response;
    }
    @Override
    protected void onPostExecute(String result) {

        data=result;
        System.out.println(data);
        System.out.println("jfghhhjj");

    }
    public String returnonoff()
    {
        if (data.equals("1")) {
            return "on";

        } else {
            return "off";
        }

    }
    public String returnsetonoff()
    {
        System.out.println(data);
        return data;
    }
}



