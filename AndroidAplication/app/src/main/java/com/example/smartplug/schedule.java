package com.example.smartplug;

import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.webkit.WebView;
import android.widget.EditText;
import android.widget.TextView;

public class schedule extends AppCompatActivity {

    EditText timeStart,timeEnd;
    TextView t1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_schedule);
        timeStart = (EditText) findViewById(R.id.editText);
        timeEnd = (EditText) findViewById(R.id.editText2);
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    public void dosomething(View view){
        String timestart= timeStart.getText().toString();
        String timeend= timeEnd.getText().toString();
        WebView myWebView = (WebView) findViewById(R.id.bad);
        myWebView.loadUrl("https://sriki007.pythonanywhere.com/androidgetscheduledata?timestart="+timestart+"&timeend="+timeend);
    }

}
