package com.example.pimonitor;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    Button btnPiMonitor, btnPiCamera;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        getSupportActionBar().setTitle("PiMonitor");


        btnPiMonitor = (Button)findViewById(R.id.btnPiMonitor);
        btnPiMonitor.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent piMonitor = new Intent(MainActivity.this, PiMonitor.class);
                startActivity(piMonitor);
            }
        });


        btnPiCamera = (Button)findViewById(R.id.btnPiCamera);
        btnPiCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent piCamera = new Intent(MainActivity.this, PiCamera.class);
                startActivity(piCamera);
            }
        });



    }
}
